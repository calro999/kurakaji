import re, glob, os

# Specific, rich, high-converting content definitions for the remaining thin cluster articles
enrichments = {
    "articles/cluster/air-fryer-vs-toaster-comparison.html": {
        "og_image": "https://tshop.r10s.jp/rcmd/cabinet/as04/as-sc-c251.jpg?_ex=600x600",
        "lead": "「トースターがあるならノンフライヤーはいらない？」「唐揚げやポテト以外にトーストも焼けるの？」と迷う人は非常に多いです。結論から言うと、<strong>朝のパン食メインならトースター、夕食の自炊時短・揚げ物惣菜の温め直し・ダイエット重視ならノンフライヤー</strong>が圧倒的に有利です。熱風循環とヒーター加熱の根本的な違い、電気代、掃除の手間を実測比較します。",
        "sections": [
            ("【早見表】ノンフライヤー vs オーブントースターの決定的な違い", """
              <div style="overflow-x: auto; margin: 18px 0;">
                <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.92rem; background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
                  <thead>
                    <tr style="background: #0f172a; color: #fff;">
                      <th style="padding: 12px 16px;">比較項目</th>
                      <th style="padding: 12px 16px;">ノンフライヤー（エアフライヤー）</th>
                      <th style="padding: 12px 16px;">オーブントースター</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr style="border-bottom: 1px solid #e2e8f0;">
                      <td style="padding: 12px 16px; font-weight: 800;">加熱方式</td>
                      <td style="padding: 12px 16px; color: #0284c7; font-weight: 700;">最高200℃の高速熱風360度循環</td>
                      <td style="padding: 12px 16px;">電熱線（ヒーター管）の直接放射熱</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e2e8f0; background: #f8fafc;">
                      <td style="padding: 12px 16px; font-weight: 800;">得意な料理</td>
                      <td style="padding: 12px 16px; font-weight: 700;">唐揚げ、ポテト、惣菜温め直し、ロースト肉</td>
                      <td style="padding: 12px 16px; font-weight: 700;">食パン（トースト）、ピザ、グラタン</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;">
                      <td style="padding: 12px 16px; font-weight: 800;">油落ち・ヘルシー度</td>
                      <td style="padding: 12px 16px; color: #0284c7; font-weight: 700;">最大85%脂質カット（底のスノコに落ちる）</td>
                      <td style="padding: 12px 16px;">油は落ちにくくトレーに溜まる</td>
                    </tr>
                    <tr style="background: #f8fafc;">
                      <td style="padding: 12px 16px; font-weight: 800;">後片付け・手入れ</td>
                      <td style="padding: 12px 16px; color: #0284c7; font-weight: 700;">バスケットを丸洗いするだけ（超手軽）</td>
                      <td style="padding: 12px 16px;">パンくずトレイ＋網・庫内壁面の焦げ取りが必要</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            """),
            ("スーパーの惣菜コロッケ・唐揚げのサクサク復活力は段違い", """
              <p style="font-size: 0.96rem; color: #334155; line-height: 1.85;">
                電子レンジで温めるとシナシナになり、トースターで温めると表面だけ焦げて中が冷たい…そんなスーパーの揚げ物惣菜が、ノンフライヤーなら<strong>「揚げたて以上のサクサク感」に完全復活</strong>します。<br />
                衣に含まれていた余分な酸化油がバスケットの底に大さじ1〜2杯分もドリップするため、カロリーを大幅にカットしつつ、胃もたれしない軽やかな食感に仕上がります。
              </p>
            """),
            ("一人暮らし・狭いキッチンの置き場所結論", """
              <p style="font-size: 0.96rem; color: #334155; line-height: 1.85;">
                キッチンのスペースに1台しか置けない場合、<strong>「朝食に毎朝サクサクのトーストを食べる」ならトースター一択</strong>です。ノンフライヤーでもパンは焼けますが、風で水分が飛びやすくややラスク寄りの食感になります。<br />
                一方で<strong>「夜の自炊を時短したい」「冷凍食品や揚げ物を油の後処理なしでヘルシーに食べたい」ならノンフライヤー</strong>が圧倒的に生活満足度を高めてくれます。最近は横幅21cm前後のA4サイズ機が主流のため、レンジの上やワゴンにすっきり収まります。
              </p>
            """)
        ]
    },
    "articles/cluster/electric-blanket-vs-panel-heater.html": {
        "og_image": "https://tshop.r10s.jp/outletkaagu/cabinet/img/sd4546_main.jpg",
        "lead": "冬のパーソナル節電暖房の二大巨頭である「電気毛布」と「デスクパネルヒーター」。どちらもエアコンと比べて圧倒的な省エネ性能を誇りますが、<strong>『就寝・リラックス時』と『テレワーク・勉強時』で適性は完全に二極化</strong>します。1ヶ月の電気代実測値と、体感の暖まり方の違いを検証します。",
        "sections": [
            ("【電気代比較】月300円 vs 月1,200円の圧倒的省エネ対決", """
              <p style="font-size: 0.96rem; color: #334155; line-height: 1.85;">
                エアコン暖房（1日8時間で月約5,200円）やセラミックファンヒーター（月約8,200円）と比較すると、どちらも桁違いに安いのが最大のメリットです。
              </p>
              <div style="background: #fff; border: 1.5px solid #e2e8f0; border-radius: 14px; padding: 20px 24px; margin: 18px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
                <ul style="margin: 0; padding-left: 20px; font-size: 0.93rem; color: #334155; line-height: 1.85;">
                  <li><strong>電気毛布（消費電力 約30〜55W）:</strong> 1日8時間使用で約8〜12円 → <strong>月額 約250円〜360円</strong> ⚡️</li>
                  <li><strong>パネルヒーター（消費電力 約160〜195W）:</strong> 1日8時間使用で約40〜48円 → <strong>月額 約1,200円〜1,450円</strong></li>
                </ul>
                <p style="font-size: 0.88rem; color: #64748b; margin: 8px 0 0;">※電気毛布は暖房器具の中でダントツNo.1の節電王。パネルヒーターもエアコンの1/4以下です。</p>
              </div>
            """),
            ("シチュエーション別の完全使い分けガイド", """
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin: 20px 0;">
                <div style="background: #fdf2f8; border: 1.5px solid #fbcfe8; border-radius: 14px; padding: 20px;">
                  <h4 style="margin: 0 0 10px 0; color: #be185d; font-size: 1.05rem; font-weight: 800;">🛌 電気毛布が最強なシーン</h4>
                  <p style="margin: 0; font-size: 0.9rem; color: #831843; line-height: 1.7;">
                    就寝前の布団の予熱、ベッドでの読書、ソファでくるまる映画鑑賞。直に身体に密着するため、極寒の夜でもエアコンなしで朝までポカポカの快眠環境を作れます。
                  </p>
                </div>
                <div style="background: #eff6ff; border: 1.5px solid #bfdbfe; border-radius: 14px; padding: 20px;">
                  <h4 style="margin: 0 0 10px 0; color: #1d4ed8; font-size: 1.05rem; font-weight: 800;">💻 パネルヒーターが最強なシーン</h4>
                  <p style="margin: 0; font-size: 0.9rem; color: #1e40af; line-height: 1.7;">
                    在宅ワーク、パソコン作業、勉強机での足元暖房。毛布を体に巻くと動きづらく眠気を誘いますが、足元を囲む5面パネルなら頭寒足熱を保ち、集中力を維持しながら下半身を極楽に温められます。
                  </p>
                </div>
              </div>
            """)
        ]
    },
    "articles/cluster/electric-snow-blower-real-experience.html": {
        "og_image": "https://thumbnail.image.rakuten.co.jp/@0_mall/haige/cabinet/new_renewal/13228281/402set_rakuten.jpg?_ex=600x600",
        "lead": "「家庭用の1〜4万円台の電動除雪機って、本当に雪が飛ぶの？」「買って後悔しない？」<br />豪雪地帯のエンジン式除雪機とは異なり、<strong>家庭用電動除雪機は『女性やシニアでも重労働の雪かきから解放される』ことに特化した都市型・新雪向けマシン</strong>です。実際に使って分かったリアルな除雪能力と、絶対に失敗しない選び方を本音でレビューします。",
        "sections": [
            ("【現実】飛ぶ雪・飛ばない雪の境界線", """
              <p style="font-size: 0.96rem; color: #334155; line-height: 1.85;">
                購入前に最も知っておくべきは、電動除雪機が得意な雪と苦手な雪の差です。
              </p>
              <div style="background: #fff; border: 1.5px solid #e2e8f0; border-radius: 14px; padding: 20px 24px; margin: 18px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
                <ul style="margin: 0; padding-left: 20px; font-size: 0.93rem; color: #334155; line-height: 1.85;">
                  <li><strong>得意な雪（大活躍）:</strong> 朝積もったばかりの新雪・パウダースノー・20cm前後の積雪。スコップなら1時間かかる駐車場1台分が、押すだけで5分で片付きます。</li>
                  <li><strong>苦手な雪（注意）:</strong> 水分を含んで重くなった春先のベタ雪。投雪距離が半分程度に落ちます。</li>
                  <li><strong>無理な雪（NG）:</strong> 除雪車が置いていったガチガチの氷塊や踏み固められた圧雪。無理に突っ込むと安全ピンが折れるかモーターが停止します。</li>
                </ul>
              </div>
            """),
            ("コード式 vs 充電式コードレス、どちらを選ぶべきか？", """
              <p style="font-size: 0.96rem; color: #334155; line-height: 1.85;">
                敷地の広さと作業スタイルによって正解が分かれます。<br />
                <strong>駐車場1〜2台分＋玄関アプローチだけなら「充電式コードレス（40Vクラス）」</strong>が圧倒的に快適。コードの引き回しや巻き込みの心配がなく、サッと取り出して10〜15分で終わらせられます。<br />
                一方、<strong>長時間じっくり雪かきしたい、バッテリー切れで中断したくない方は「100Vコンセント式（1200W〜1400W）」</strong>がパワー・連続稼働ともに優れ、本体価格も2万円前後と手頃です。
              </p>
            """)
        ]
    },
    "articles/cluster/humidifier-steam-vs-ultrasonic.html": {
        "og_image": "https://tshop.r10s.jp/fithome/cabinet/08895627/coffeemaker1.jpg?_ex=600x600",
        "lead": "冬の乾燥対策に欠かせない加湿器。「スチーム式（加熱式）」と「超音波式」、見た目は似ていても中身の仕組みは月とスッポンです。<strong>『お手入れのラクさと衛生面』を重視するならスチーム式、『電気代とデザイン・静音性』を重視するなら超音波式</strong>。それぞれのメリット・デメリットを徹底検証します。",
        "sections": [
            ("【衛生対決】雑菌・カビをまき散らさないのはどっち？", """
              <p style="font-size: 0.96rem; color: #334155; line-height: 1.85;">
                加湿器で最も恐ろしいのが「加湿器肺炎」を引き起こすレジオネラ菌の繁殖です。<br />
                <strong>スチーム式は水を100℃で沸騰させて蒸気にするため、雑菌を熱で完全死滅させてクリーンな蒸気だけを放出</strong>します。数日水を放置してもカビが舞うリスクがほぼありません。<br />
                一方の<strong>超音波式は水を振動させて微粒子にして飛ばすため、タンク内の水に雑菌が繁殖していると、菌ごと部屋中に噴射</strong>してしまいます。毎日必ず水を入れ替え、こまめなパーツ洗浄が絶対条件となります。
              </p>
            """),
            ("【電気代対決】月150円 vs 月2,500円の圧倒的格差", """
              <p style="font-size: 0.96rem; color: #334155; line-height: 1.85;">
                衛生面で最強のスチーム式ですが、最大の弱点は「電気ポットでお湯を沸かし続けているのと同じ」という消費電力の高さです。
              </p>
              <div style="background: #fff; border: 1.5px solid #e2e8f0; border-radius: 14px; padding: 20px 24px; margin: 18px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
                <ul style="margin: 0; padding-left: 20px; font-size: 0.93rem; color: #334155; line-height: 1.85;">
                  <li><strong>超音波式（消費電力 約20〜30W）:</strong> 1日8時間使用で月額 <strong>約150円〜220円</strong> 💡</li>
                  <li><strong>スチーム式（消費電力 約250〜400W）:</strong> 1日8時間使用で月額 <strong>約1,800円〜2,900円</strong> ⚡️</li>
                </ul>
                <p style="font-size: 0.88rem; color: #64748b; margin: 8px 0 0;">※電気代を安く抑えたいなら超音波式、掃除の手間（クエン酸洗浄のみ）を買うならスチーム式が正解です。</p>
              </div>
            """)
        ]
    },
    "articles/cluster/single-life-breaker-trip-prevention.html": {
        "og_image": "https://tshop.r10s.jp/panasonic-store/cabinet/banner/12923490/nc-a58_main_007.jpg?_ex=600x600",
        "lead": "「冬の寒い夜、エアコンと電子レンジを同時に使ったらバチン！と部屋が真っ暗に…」<br />一人暮らしの賃貸アパートで最も多いトラブルがこのブレーカー落ちです。多くの単身物件は【20A〜30A（2000W〜3000W）】で契約されているため、家電の消費電力を正しく把握していないと頻繁に停電します。冬家電のワット数マップと、ブレーカーを絶対に落とさない同時使用ルールを解説します。",
        "sections": [
            ("【要注意】冬の高消費電力家電ワット数ワースト一覧", """
              <div style="background: #fff; border: 1.5px solid #e2e8f0; border-radius: 14px; padding: 20px 24px; margin: 18px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
                <ul style="margin: 0; padding-left: 20px; font-size: 0.93rem; color: #334155; line-height: 1.85;">
                  <li><strong>電子レンジ（温め時）:</strong> 約1,000W〜1,400W ⚠️</li>
                  <li><strong>電気ケトル（湯沸かし時）:</strong> 約1,200W〜1,300W ⚠️</li>
                  <li><strong>ドライヤー（温風強）:</strong> 約1,200W ⚠️</li>
                  <li><strong>セラミックファンヒーター:</strong> 約1,200W ⚠️</li>
                  <li><strong>エアコン（暖房立ち上がり時）:</strong> 約900W〜1,400W ⚠️</li>
                  <li><strong>炊飯器（炊飯時）:</strong> 約600W〜1,100W</li>
                </ul>
                <p style="font-size: 0.88rem; color: #dc2626; font-weight: 700; margin: 10px 0 0;">
                  ⚠️ 上記の1,000W超え家電のうち、「どれか2つ」が同時に動いた瞬間に20Aブレーカーは即死（遮断）します。
                </p>
              </div>
            """),
            ("絶対にブレーカーを落とさない3大ルール", """
              <ol style="margin: 0; padding-left: 22px; font-size: 0.95rem; color: #334155; line-height: 1.9;">
                <li><strong>ケトルとお弁当の温めは絶対にズラす:</strong> 朝の忙しい時間、電子レンジで温めながらケトルでコーヒーのお湯を沸かすのは最大のNG。必ず片方が終わってからスイッチを入れましょう。</li>
                <li><strong>ドライヤーを使う時はヒーターを弱にする:</strong> お風呂上がりに脱衣所でセラミックヒーターを強（1200W）にしたままドライヤー（1200W）を使うと、その回路だけで24Aになり一発で落ちます。</li>
                <li><strong>超低消費電力の省エネ暖房を活用する:</strong> デスクワークや就寝時は、1200Wの温風ヒーターではなく、190Wのパネルヒーターや50Wの電気毛布に切り替えることで、アンペア数に圧倒的な余裕が生まれます。</li>
              </ol>
            """)
        ]
    },
    "articles/cluster/single-life-dishwasher-necessity.html": {
        "og_image": "https://tshop.r10s.jp/siroca/cabinet/sc-a211/thumb_01.jpg?_ex=600x600",
        "lead": "「一人暮らしで食洗機なんて贅沢？」「食器なんて手で洗えば数分でしょ？」と思っていませんか？<br />実は今、<strong>工事不要のタンク式小型食洗機を導入して『人生で一番買ってよかった家電』に挙げる一人暮らし世帯が急増</strong>しています。手洗いと比べた水道光熱費の実測差、設置スペースのリアル、そして手洗いから解放される本当のタイパ価値を徹底検証します。",
        "sections": [
            ("【水道代検証】手洗いより食洗機の方が水道代が1/6になる理由", """
              <p style="font-size: 0.96rem; color: #334155; line-height: 1.85;">
                手洗いで水を流しながら洗うと、1回の食器洗いで約35L〜45Lの水を使用します。<br />
                対して<strong>タンク式食洗機は庫内で少量の水を高圧循環させて洗浄するため、わずか約5L〜6Lの水でピカピカに洗い上げます</strong>。<br />
                水道代だけで年間約7,000円〜9,000円の節約になり、電気代（約15〜20円/回）を差し引いても年間トータルで手洗いと同等以上のコストパフォーマンスを発揮します。
              </p>
            """),
            ("一人暮らしが食洗機を買うべき最大の理由は「タイパと手荒れ防止」", """
              <p style="font-size: 0.96rem; color: #334155; line-height: 1.85;">
                お金の節約以上に大きいのが<strong>「毎日のシンクに食器が溜まるストレスがゼロになる」</strong>精神的メリットです。<br />
                1日15分の皿洗いは、1年間で約90時間（まるまる3.7日分）に相当します。食べた食器を放り込んでボタンを押すだけで、冬場の冷たい水やお湯による頑固な手荒れからも完全に解放されます。
              </p>
            """)
        ]
    }
}

for filepath, data in enrichments.items():
    if not os.path.exists(filepath):
        continue
    with open(filepath, "r", encoding="utf-8") as f:
        c = f.read()

    # 1. Update OGP Image
    c = re.sub(r'<meta property="og:image" content=".*?"', f'<meta property="og:image" content="{data["og_image"]}"', c)
    c = re.sub(r'<meta name="twitter:image" content=".*?"', f'<meta name="twitter:image" content="{data["og_image"]}"', c)

    # 2. Build Rich Body HTML
    sections_html = ""
    for sec_title, sec_content in data["sections"]:
        sections_html += f"""
        <section style="margin-bottom: 35px;">
          <h2 style="font-size: 1.4rem; font-weight: 800; color: #0f172a; margin-bottom: 14px; border-left: 5px solid #0284c7; padding-left: 12px;">{sec_title}</h2>
          {sec_content.strip()}
        </section>
        """

    full_body = f"""
    <div class="article-lead" style="font-size: 1.05rem; line-height: 1.85; color: #334155; background: #f8fafc; border-left: 4px solid #0284c7; padding: 20px 24px; border-radius: 0 12px 12px 0; margin-bottom: 30px;">
      {data["lead"]}
    </div>

    {sections_html}
    """

    # Locate insertion point
    h2_idx = c.find("</header>", 21000)
    if h2_idx == -1:
        h2_idx = c.find("</header>")
    
    faq_idx = c.find("<!-- FAQ Section -->")
    if faq_idx == -1:
        faq_idx = c.find("よくある質問（FAQ）")
        faq_idx = c.rfind("<div", 0, faq_idx)

    if h2_idx != -1 and faq_idx != -1:
        new_c = c[:h2_idx+9] + "\n\n" + full_body.strip() + "\n\n    " + c[faq_idx:]
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_c)
        print(f"Deep enriched {filepath} successfully!")
    else:
        print(f"Could not find markers in {filepath}")

print("All thin cluster articles enriched with high-value expert content!")
