from flask import url_for
class URLOptimize:
    def optimize_urls(urls_list,no_optimize=False):
        urls_dict = {}
        for url in urls_list:
            if not no_optimize:
                if url.startswith('https://'):
                    url = url.replace('https://','http://',1)
                if url.startswith('http://en.wikipedia'):
                    url = url.replace('en.wiki','en.m.wiki',1)
            # NOTE: Imagify URL
            # TODO: tight coupling: bad design!
            url_img = url_for('imagify_blueprint.imagify',url=url)
            urls_dict[url] = url_img
        return urls_dict
