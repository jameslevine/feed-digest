"""Generate feeds.opml (this repo) and the NetNewsWire copy from one list.
Run: python3 gen_feeds.py   then commit. GitHub release feeds are swapped for PyPI in the repo copy
(the routine's environment can only reach GitHub for this repo) or dropped if no PyPI package exists."""
from pathlib import Path
from xml.sax.saxutils import escape as e

def gh(name, repo, pkg=None): return (f"{name} releases", f"https://github.com/{repo}/releases.atom", f"https://github.com/{repo}/releases", pkg)
def f(name, xml, html): return (name, xml, html, None)

F = {
 "Python": [
   f("PEPs (new and updated)", "https://peps.python.org/peps.rss", "https://peps.python.org/"),
   f("Discourse: PEPs", "https://discuss.python.org/c/peps/19.rss", "https://discuss.python.org/c/peps/19"),
   f("Python Insider (releases)", "https://blog.python.org/feeds/posts/default", "https://blog.python.org/"),
   f("Real Python", "https://realpython.com/atom.xml", "https://realpython.com/"),
   f("Astral blog (uv, ruff)", "https://astral.sh/blog/rss.xml", "https://astral.sh/blog"),
   gh("uv", "astral-sh/uv", "uv"), gh("ruff", "astral-sh/ruff", "ruff"), gh("pydantic", "pydantic/pydantic", "pydantic"),
   gh("FastAPI", "fastapi/fastapi", "fastapi"), gh("httpx", "encode/httpx", "httpx"), gh("pytest", "pytest-dev/pytest", "pytest"),
 ],
 "JavaScript and TypeScript": [
   f("Node.js blog", "https://nodejs.org/en/feed/blog.xml", "https://nodejs.org/en/blog"),
   f("TypeScript blog", "https://devblogs.microsoft.com/typescript/feed/", "https://devblogs.microsoft.com/typescript/"),
   f("JavaScript Weekly", "https://javascriptweekly.com/rss/", "https://javascriptweekly.com/"),
   f("Node Weekly", "https://nodeweekly.com/rss/", "https://nodeweekly.com/"),
   f("web.dev", "https://web.dev/feed.xml", "https://web.dev/"),
   f("Deno blog", "https://deno.com/feed", "https://deno.com/blog"),
   f("Bun blog", "https://bun.sh/rss.xml", "https://bun.sh/blog"),
   gh("Vite", "vitejs/vite"), gh("TypeScript", "microsoft/TypeScript"),
 ],
 "React": [
   f("React blog", "https://react.dev/rss.xml", "https://react.dev/blog"),
   f("React Status (weekly)", "https://react.statuscode.com/rss", "https://react.statuscode.com/"),
   f("Next.js blog", "https://nextjs.org/feed.xml", "https://nextjs.org/blog"),
   f("Overreacted (Dan Abramov)", "https://overreacted.io/rss.xml", "https://overreacted.io/"),
   f("Josh Comeau", "https://www.joshwcomeau.com/rss.xml", "https://www.joshwcomeau.com/"),
   f("Kent C. Dodds", "https://kentcdodds.com/blog/rss.xml", "https://kentcdodds.com/blog"),
   f("TanStack blog", "https://tanstack.com/rss.xml", "https://tanstack.com/blog"),
   gh("React", "facebook/react"), gh("React Router", "remix-run/react-router"),
 ],
 "Rust": [
   f("Rust blog (releases, announcements)", "https://blog.rust-lang.org/feed.xml", "https://blog.rust-lang.org/"),
   f("Inside Rust (project internals)", "https://blog.rust-lang.org/inside-rust/feed.xml", "https://blog.rust-lang.org/inside-rust/"),
   f("This Week in Rust", "https://this-week-in-rust.org/rss.xml", "https://this-week-in-rust.org/"),
   f("Rust users forum: announcements", "https://users.rust-lang.org/c/announcements/6.rss", "https://users.rust-lang.org/c/announcements"),
   f("Tokio blog", "https://tokio.rs/blog/index.xml", "https://tokio.rs/blog"),
   f("fasterthanlime", "https://fasterthanli.me/index.xml", "https://fasterthanli.me/"),
   gh("Rust", "rust-lang/rust"), gh("Cargo", "rust-lang/cargo"),
 ],
 "Go": [
   f("Go blog", "https://go.dev/blog/feed.atom", "https://go.dev/blog"),
   f("Golang Weekly", "https://golangweekly.com/rss/", "https://golangweekly.com/"),
   f("Go tags (releases)", "https://github.com/golang/go/tags.atom", "https://go.dev/doc/devel/release"),
   f("Dave Cheney", "https://dave.cheney.net/feed", "https://dave.cheney.net/"),
   f("Three Dots Labs", "https://threedots.tech/index.xml", "https://threedots.tech/"),
   f("Go Time podcast", "https://changelog.com/gotime/feed", "https://changelog.com/gotime"),
 ],
 "Java": [
   f("Inside Java (OpenJDK team)", "https://inside.java/feed.xml", "https://inside.java/"),
   f("Spring blog", "https://spring.io/blog.atom", "https://spring.io/blog"),
   f("Baeldung (incl. Java Weekly)", "https://feeds.feedblitz.com/baeldung", "https://www.baeldung.com/"),
   f("InfoQ Java", "https://feed.infoq.com/java/", "https://www.infoq.com/java/"),
   f("JetBrains Java annotated monthly", "https://blog.jetbrains.com/idea/feed/", "https://blog.jetbrains.com/idea/"),
 ],
 "IaC and DevOps": [
   gh("Terraform", "hashicorp/terraform"), gh("Terraform AWS provider", "hashicorp/terraform-provider-aws"),
   f("HashiCorp blog", "https://www.hashicorp.com/blog/feed.xml", "https://www.hashicorp.com/blog"),
   f("OpenTofu blog", "https://opentofu.org/blog/rss.xml", "https://opentofu.org/blog"),
   f("GitHub Changelog", "https://github.blog/changelog/feed/", "https://github.blog/changelog/"),
   f("GitHub Blog", "https://github.blog/feed/", "https://github.blog/"),
   f("AWS DevOps and Developer Productivity Blog", "https://aws.amazon.com/blogs/devops/feed/", "https://aws.amazon.com/blogs/devops/"),
   f("AWS Infrastructure and Automation Blog", "https://aws.amazon.com/blogs/infrastructure-and-automation/feed/", "https://aws.amazon.com/blogs/infrastructure-and-automation/"),
   f("Platform Engineering", "https://platformengineering.org/blog/rss.xml", "https://platformengineering.org/blog"),
   gh("tflint", "terraform-linters/tflint"), gh("trivy", "aquasecurity/trivy"), gh("conftest", "open-policy-agent/conftest"),
 ],
 "AWS": [
   f("AWS What's New", "https://aws.amazon.com/about-aws/whats-new/recent/feed/", "https://aws.amazon.com/new/"),
   f("AWS News Blog (Jeff Barr)", "https://aws.amazon.com/blogs/aws/feed/", "https://aws.amazon.com/blogs/aws/"),
   f("AWS Compute Blog", "https://aws.amazon.com/blogs/compute/feed/", "https://aws.amazon.com/blogs/compute/"),
   f("AWS Architecture Blog", "https://aws.amazon.com/blogs/architecture/feed/", "https://aws.amazon.com/blogs/architecture/"),
   f("AWS Database Blog (DynamoDB)", "https://aws.amazon.com/blogs/database/feed/", "https://aws.amazon.com/blogs/database/"),
   f("AWS Cloud Operations Blog (Organizations, Control Tower)", "https://aws.amazon.com/blogs/mt/feed/", "https://aws.amazon.com/blogs/mt/"),
   f("AWS Machine Learning Blog (Bedrock)", "https://aws.amazon.com/blogs/machine-learning/feed/", "https://aws.amazon.com/blogs/machine-learning/"),
   f("AWS Open Source Blog", "https://aws.amazon.com/blogs/opensource/feed/", "https://aws.amazon.com/blogs/opensource/"),
   f("Last Week in AWS", "https://www.lastweekinaws.com/feed/", "https://www.lastweekinaws.com/"),
   f("Yan Cui (theburningmonk)", "https://theburningmonk.com/feed/", "https://theburningmonk.com/"),
   f("Ran the Builder (Python serverless)", "https://www.ranthebuilder.cloud/blog-feed.xml", "https://www.ranthebuilder.cloud/"),
   f("All Things Distributed (Werner Vogels)", "https://www.allthingsdistributed.com/atom.xml", "https://www.allthingsdistributed.com/"),
   gh("Powertools for AWS Lambda (Python)", "aws-powertools/powertools-lambda-python", "aws-lambda-powertools"),
   gh("boto3", "boto/boto3", "boto3"), gh("moto", "getmoto/moto", "moto"),
 ],
 "AI and agents": [
   f("Simon Willison", "https://simonwillison.net/atom/everything/", "https://simonwillison.net/"),
   f("Latent Space", "https://www.latent.space/feed", "https://www.latent.space/"),
   f("Hamel Husain", "https://hamel.dev/index.xml", "https://hamel.dev/"),
   gh("Claude Code", "anthropics/claude-code"), gh("Anthropic Python SDK", "anthropics/anthropic-sdk-python", "anthropic"),
   gh("Claude Agent SDK (Python)", "anthropics/claude-agent-sdk-python", "claude-agent-sdk"),
   gh("MCP specification", "modelcontextprotocol/modelcontextprotocol"), gh("MCP Python SDK", "modelcontextprotocol/python-sdk", "mcp"),
   gh("Strands Agents", "strands-agents/sdk-python", "strands-agents"),
 ],
 "Security": [
   f("AWS Security Blog", "https://aws.amazon.com/blogs/security/feed/", "https://aws.amazon.com/blogs/security/"),
   f("AWS Security Bulletins", "https://aws.amazon.com/security/security-bulletins/rss/feed/", "https://aws.amazon.com/security/security-bulletins/"),
   f("GitHub Blog: security", "https://github.blog/security/feed/", "https://github.blog/security/"),
   f("tl;dr sec (weekly appsec roundup)", "https://tldrsec.com/feed.xml", "https://tldrsec.com/"),
   f("Trail of Bits blog", "https://blog.trailofbits.com/feed/", "https://blog.trailofbits.com/"),
   f("Google Project Zero", "https://googleprojectzero.blogspot.com/feeds/posts/default", "https://googleprojectzero.blogspot.com/"),
   f("Schneier on Security", "https://www.schneier.com/feed/atom/", "https://www.schneier.com/"),
   f("Krebs on Security", "https://krebsonsecurity.com/feed/", "https://krebsonsecurity.com/"),
   f("The Hacker News", "https://feeds.feedburner.com/TheHackersNews", "https://thehackernews.com/"),
   f("Datadog Security Labs (cloud)", "https://securitylabs.datadoghq.com/rss/feed.xml", "https://securitylabs.datadoghq.com/"),
   f("Wiz blog (cloud security)", "https://www.wiz.io/feed/rss.xml", "https://www.wiz.io/blog"),
   f("Snyk blog (supply chain)", "https://snyk.io/blog/feed/", "https://snyk.io/blog/"),
   f("NCSC UK", "https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml", "https://www.ncsc.gov.uk/"),
   f("CISA advisories", "https://www.cisa.gov/cybersecurity-advisories/all.xml", "https://www.cisa.gov/news-events/cybersecurity-advisories"),
 ],
 "AI security": [
   f("Embrace The Red (Johann Rehberger, prompt injection)", "https://embracethered.com/blog/index.xml", "https://embracethered.com/blog/"),
   f("OWASP GenAI Security Project", "https://genai.owasp.org/feed/", "https://genai.owasp.org/"),
   f("Unsupervised Learning (Daniel Miessler)", "https://danielmiessler.com/feed", "https://danielmiessler.com/"),
   f("Simon Willison: prompt injection tag", "https://simonwillison.net/tags/prompt-injection.atom", "https://simonwillison.net/tags/prompt-injection/"),
   gh("garak (LLM vulnerability scanner)", "NVIDIA/garak", "garak"),
   gh("PyRIT (Microsoft red-teaming)", "Azure/PyRIT", "pyrit"),
 ],
 "Engineering practice": [
   f("The Pragmatic Engineer", "https://newsletter.pragmaticengineer.com/feed", "https://newsletter.pragmaticengineer.com/"),
   f("Martin Fowler", "https://martinfowler.com/feed.atom", "https://martinfowler.com/"),
   f("Increment / Stripe engineering", "https://stripe.com/blog/feed.rss", "https://stripe.com/blog/engineering"),
   f("Google Testing Blog", "https://testing.googleblog.com/feeds/posts/default", "https://testing.googleblog.com/"),
 ],
}

def opml(title, for_digest):
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<opml version="2.0">', f'  <head><title>{e(title)}</title></head>', '  <body>']
    for folder, feeds in F.items():
        rows = []
        for name, xml, html, pkg in feeds:
            if for_digest and "github.com" in xml:
                if not pkg: continue
                name, xml, html = f"{name.replace(' releases', '')} (PyPI)", f"https://pypi.org/rss/project/{pkg}/releases.xml", f"https://pypi.org/project/{pkg}/"
            rows.append(f'      <outline text="{e(name)}" type="rss" xmlUrl="{e(xml)}" htmlUrl="{e(html)}"/>')
        if rows: out += [f'    <outline text="{e(folder)}">', *rows, '    </outline>']
    out += ['  </body>', '</opml>', '']
    return "\n".join(out)

Path("feeds.opml").write_text(opml("feed-digest sources", True))
nnw = Path.home() / ".config/netnewswire/feeds.opml"
nnw.write_text(opml("James's feeds", False))
import xml.dom.minidom
for p in (Path("feeds.opml"), nnw): xml.dom.minidom.parse(str(p))
print("digest feeds:", Path("feeds.opml").read_text().count("xmlUrl="), "| reader feeds:", nnw.read_text().count("xmlUrl="), "| folders:", ", ".join(F))
