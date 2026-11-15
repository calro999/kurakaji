// Vercel Serverless Function: Rakuten Item Search API Proxy
export default async function handler(req, res) {
  // CORS configuration
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const { keyword, hits = 30, page = 1, sort = 'standard' } = req.query;

  const appId = process.env.RAKUTEN_APP_ID;
  const accessKey = process.env.RAKUTEN_ACCESS_KEY;
  const affiliateId = process.env.RAKUTEN_AFFILIATE_ID;

  if (!appId || !accessKey) {
    return res.status(500).json({
      error: 'Rakuten API credentials (RAKUTEN_APP_ID, RAKUTEN_ACCESS_KEY) are not configured in Vercel Environment Variables.'
    });
  }

  const searchKeyword = keyword || '小型家電 暮らし 便利';

  const params = new URLSearchParams({
    applicationId: appId,
    accessKey: accessKey,
    keyword: searchKeyword,
    format: 'json',
    hits: String(hits),
    page: String(page)
  });

  if (affiliateId) {
    params.append('affiliateId', affiliateId);
  }

  if (sort === 'sales') {
    // 楽天APIのレビュー件数順または標準
    params.append('sort', '-reviewCount');
  } else if (sort === 'priceAsc') {
    params.append('sort', '+itemPrice');
  } else if (sort === 'priceDesc') {
    params.append('sort', '-itemPrice');
  }

  const apiUrl = `https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20260401?${params.toString()}`;

  try {
    const response = await fetch(apiUrl, {
      headers: {
        'Accept': 'application/json'
      }
    });

    if (!response.ok) {
      const errText = await response.text();
      return res.status(response.status).json({
        error: 'Failed to fetch from Rakuten API',
        details: errText
      });
    }

    const data = await response.json();
    
    // Clean and normalize items for the frontend
    const cleanedItems = (data.Items || []).map((wrapper) => {
      const item = wrapper.Item || wrapper;
      
      // Clean item name
      let name = item.itemName || '';
      name = name
        .replace(/【[^】]*】/g, '')
        .replace(/\[[^\]]*\]/g, '')
        .replace(/（[^）]*）/g, '')
        .replace(/\([^\)]*\)/g, '')
        .replace(/クーポン(?:で|\s*利用で|\s*配布中|\s*対象)?\s*[0-9,]+円?(?:OFF|off)?/gi, '')
        .replace(/P[0-9]+倍/gi, '')
        .replace(/ポイント[0-9]+倍/gi, '')
        .replace(/送料無料/g, '')
        .replace(/即納/g, '')
        .replace(/あす楽/g, '')
        .replace(/お買い物マラソン/g, '')
        .replace(/楽天(?:1位|ランキング1位|デイリー1位)/g, '')
        .replace(/[0-9]+%OFF/gi, '')
        .replace(/[0-9]+％OFF/gi, '')
        .replace(/★[0-9\.]+★?/g, '')
        .replace(/レビュー特典/g, '')
        .replace(/公式(?:店)?/g, '')
        .trim();

      // Highest quality image resolution
      let img = '';
      if (item.mediumImageUrls && item.mediumImageUrls.length > 0) {
        const first = item.mediumImageUrls[0];
        img = typeof first === 'string' ? first : (first.imageUrl || '');
      } else if (item.smallImageUrls && item.smallImageUrls.length > 0) {
        const first = item.smallImageUrls[0];
        img = typeof first === 'string' ? first : (first.imageUrl || '');
      }
      if (img) {
        img = img.replace(/^http:\/\//i, 'https://').replace(/_ex=[0-9]+x[0-9]+/, '_ex=500x500');
      }

      // Generate robust affiliate link
      let affLink = item.affiliateUrl || '';
      if (!affLink && affiliateId && item.itemUrl) {
        const encUrl = encodeURIComponent(item.itemUrl);
        affLink = `https://hb.afl.rakuten.co.jp/hgc/${affiliateId}/?pc=${encUrl}&m=${encUrl}`;
      } else if (!affLink) {
        affLink = item.itemUrl || 'https://www.rakuten.co.jp/';
      }

      return {
        itemCode: item.itemCode,
        title: name || item.itemName,
        rawTitle: item.itemName,
        price: item.itemPrice,
        priceFormatted: Number(item.itemPrice || 0).toLocaleString() + '円',
        imageUrl: img,
        affiliateUrl: affLink,
        shopName: item.shopName,
        reviewCount: item.reviewCount || 0,
        reviewAverage: item.reviewAverage || 0,
        itemCaption: item.itemCaption || '',
        asuraku: item.asurakuFlag === 1,
        postageFree: item.postageFlag === 0
      };
    });

    return res.status(200).json({
      count: data.count || cleanedItems.length,
      page: data.page || page,
      hits: data.hits || hits,
      items: cleanedItems
    });
  } catch (error) {
    return res.status(500).json({
      error: 'Internal Server Error',
      message: error.message
    });
  }
}
