import urllib.request, json

def test_fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            content_type = resp.headers.get("Content-Type", "")
            return resp.status == 200 and "image" in content_type
    except Exception as e:
        return False

# Test sample unsplash image
test_url = "https://images.unsplash.com/photo-1545259741-2ea3ebf61fa3?w=800&auto=format&fit=crop&q=80"
ok = test_fetch(test_url)
print(f"Unsplash test fetch: {ok}")
