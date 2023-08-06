
RE_TAG_SCRIPT = r'<script[^>]*>{1}[^<]*</script>'
RE_TAG_STYLE = r'<style[^>]*>{1}[^<]*</style>'
RE_TAG_COMMENT = r'<!--.*-->{1}?'
RE_TAG_COMMON = r'<[^>]*>[^<]*</.*>'
RE_TAG_OPEN = r'</?[^>]*>'
#RE_TAG_ALL = r'(?mi:<script[^>]*>{1}[^<]*</script>|<style[^>]*>{1}[^<]*</style>|<!--.*(?:-->){1}?|<[^>]+>[^<]*</>|<[^>]>)'
RE_TAG_ALL = r'(?i:<script[^>]*>{1}[^<]*[<.]*[^<]*</script>|<style[^>]*>{1}[^<]*[<.]*[^<]*</style>|<!--.*(?:-->){1}?|<[^>]+>)'
RE_HTML_ENTITY = r'(?i:&nbsp;)'