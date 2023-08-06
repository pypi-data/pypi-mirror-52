comk_django_account
========================
comk个人开发的account模型，用于构建RSA-SHA256验证的权限系统

现有功能
========================

1. model构建
-------------------------------------------------------------------------------
#. 先在settings中进行配置::

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'comk_django_account.apps.ComkDjangoAccountConfig', # 加上这一行
    ]

#. 再执行 migrate 命令::


    python manage.py

2. 添加账户
-------------------------------------------------------------------------------
#. 在urls.py下加上url配置::

    from django.conf.urls import url, include
    from django.contrib import admin

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^', include('comk_django_account.urls')),
    ]

#. 通过API创建账户::

    url= '/acount_action/'
    request_data = dict(
        method='account.add', # 必传参数
        description='测', # 账户描述
        appid='381', # 账户id
        pri_key=pri_key, # 私钥
        own_public_key=own_public_key, # 公钥
        other_public_key=other_public_key, # 对方公钥
    )
    request.post(url,json=request_data)


3. 设置加密解密Key
-------------------------------------------------------------------------------
对于某些数据来说，是非常重要的，那么就不能明文存储在数据库中，必须加密存储，而且，为了方便使用，必须是可逆加密。

在此使用的加密算法是AES对称加密，这就涉及到一个问题，Key的值。

这里使用了一个默认的值，但是对于生产的项目来说，不建议使用默认的值，在此提供一个设置该Key值的方法，需要在setting文件中配置，如下::

    setting.py

    from comk_django_account import set_account_aes_key
    set_account_aes_key(Key)  # Key值在本包内，限定为32位。



4. 权限校验
-------------------------------------------------------------------------------
#. 对于服务方来说，这里提供一个默认的权限校验方式，只需要加上装饰器即可，使用方法如下::


    from comk_django_account.views.utils.app_check import request_to_response
    @method_decorator(request_to_response, name='dispatch')  # 用户访问权限校验，以及业务正常失败处理
    class Server(View):
        """
        提供的服务

        """

#. 默认的权限校验方式的要求::

    1. 权限校验必须限定为POST请求，且交互数据必须是JSON字符串。
    2. 必须有appid、method、timestamp、content、sign字段
    3. timestamp的格式为'2019-01-01 00:00:00'
    4. content必须是键值对
    5. 该装饰器已经确定返回JsonResponse，因为原Server只需要返回dict数据就行，装饰器会进行封装

#. 可以根据此检验方式实现自己的权限校验方法

5. 调用服务
-------------------------------------------------------------------------------
#. 与上面的默认权限校验相对，对于调用方来说，需要加签名通过认证::

    from comk_django_account.views.utils.sign_utils import get_sign
    def get_sign(pri_key, r_data):
        '''
        获取签名

        :param pri_key: 私钥
        :param r_data: 一个dict数据
        :return:
        '''

    取得键为sign、值为签名值的键值对

#. 为方便调用者，可使用 params_utils 下的 build_request_params 或 make_params_with_sign 方法，直接构造出请求数据。

6. 其他
-------------------------------------------------------------------------------
需要注意的是，权限校验与调用方法是需要对应的。例如，服务方单独实现了一个校验方法，而调用方使用默认的加签方法，这是不行的。
