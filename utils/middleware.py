# _*_ coding:utf-8 _*_ 


# 在此中间件类中设置session,到login_check视图函数中判断
class UrlPathRecordMiddleWare(object):
    '''记录用户访问的中间件类'''
    # 不用要记录的url
    exclude_path = ['/user/login/', '/user/logout/', '/user/register']
    # 排除ajax请求的地址
    # request.is_ajax() 判断是不是一个ajax发起的请求
    # request.path 获取用户访问的url地址

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        # 次函数中访问的地址
        if request.path not in UrlPathRecordMiddleWare.exclude_path and not request.is_ajax():
            # 记录这个地址
            request.session['pre_url_path'] = request.path



