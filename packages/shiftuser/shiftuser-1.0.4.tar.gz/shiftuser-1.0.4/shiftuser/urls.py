from boiler.routes.route import route

"""
User URLs
This is a set of urls that provide user registration and management
functionality. You can import them all at once and attach to your app
urls file like this:

    > from shiftuser.urls import user_urls
    > urls = dict()
    > urls.update(user_urls)

"""

user_urls = dict()

# user generic
user_urls['/login-password/'] = route('shiftuser.views.Login', 'user.login', ['GET', 'POST'])
user_urls['/login/'] = route('shiftuser.views.SocialLogin', 'user.social_login')
user_urls['/logout/'] = route('shiftuser.views.Logout', 'user.logout')
user_urls['/register/'] = route('shiftuser.views.Register', 'user.register', ['GET', 'POST'])
user_urls['/register/success/'] = route('shiftuser.views.RegisterSuccess', 'user.register.success')
user_urls['/register/fail/'] = route('shiftuser.views.RegisterFail', 'user.register.fail')

# confirm email
user_urls['/user/confirm-email/'] = route('shiftuser.views.ConfirmEmailRequest', 'user.confirm.email.request', ['GET', 'POST'])
user_urls['/user/confirm-email/unconfirmed/'] = route('shiftuser.views.ConfirmEmailUnconfirmed', 'user.confirm.email.unconfirmed')
user_urls['/user/confirm-email/resent/'] = route('shiftuser.views.ConfirmEmailResendOk', 'user.confirm.email.resend.ok')
user_urls['/user/confirm-email/already-confirmed/'] = route('shiftuser.views.ConfirmEmailResendAlreadyConfirmed', 'user.confirm.email.resend.already_confirmed')
user_urls['/user/confirm-email/expired/'] = route('shiftuser.views.ConfirmEmailExpired', 'user.confirm.email.expired')
user_urls['/user/confirm-email/<link>/'] = route('shiftuser.views.ConfirmEmail', 'user.confirm.email.link')

# recover password
user_urls['/user/recover-password/'] = route('shiftuser.views.RecoverPasswordRequest', 'user.recover.password.request', ['GET', 'POST'])
user_urls['/user/recover-password/sent/'] = route('shiftuser.views.RecoverPasswordRequestOk', 'user.recover.password.sent')
user_urls['/user/recover-password/expired/'] = route('shiftuser.views.RecoverPasswordExpired', 'user.recover.password.expired')
user_urls['/user/recover-password/<link>/'] = route('shiftuser.views.RecoverPassword', 'user.recover.password.link', ['GET', 'POST'])

# social
user_urls['/login/social/facebook/auth/'] = route('shiftuser.views_social.FacebookAuthorize', 'social.facebook.auth')
user_urls['/login/social/facebook/'] = route('shiftuser.views_social.FacebookHandle', 'social.facebook.handle')
user_urls['/login/social/vk/auth/'] = route('shiftuser.views_social.VkontakteAuthorize', 'social.vkontakte.auth')
user_urls['/login/social/vk/'] = route('shiftuser.views_social.VkontakteHandle', 'social.vkontakte.handle')
user_urls['/login/social/google/auth/'] = route('shiftuser.views_social.GoogleAuthorize', 'social.google.auth')
user_urls['/login/social/google/'] = route('shiftuser.views_social.GoogleHandle', 'social.google.handle')
user_urls['/login/social/instagram/auth'] = route('shiftuser.views_social.InstagramAuthorize', 'social.instagram.auth')
user_urls['/login/social/instagram/'] = route('shiftuser.views_social.InstagramHandle', 'social.instagram.handle')

# profile
user_urls['/me/'] = route('shiftuser.views_profile.Me', 'user.me')
user_urls['/user/<int:id>/'] = route('shiftuser.views_profile.ProfileHome', 'user.profile.home')
user_urls['/user/<int:id>/email/'] = route('shiftuser.views_profile.ProfileEmailChange', 'user.profile.email', ['GET', 'POST'])
user_urls['/user/<int:id>/email/resend/'] = route('shiftuser.views_profile.ProfileConfirmEmailResend', 'user.profile.email.confirm.resend')
user_urls['/user/<int:id>/password/'] = route('shiftuser.views_profile.ProfilePasswordChange', 'user.profile.password', ['GET', 'POST'])
user_urls['/user/<int:id>/social/'] = route('shiftuser.views_profile.ProfileSocial', 'user.profile.social')
user_urls['/user/social/connect-facebook/'] = route('shiftuser.views_profile.ProfileSocialConnectFacebook', 'user.social.connect.facebook')
user_urls['/user/social/connect-google/'] = route('shiftuser.views_profile.ProfileSocialConnectGoogle', 'user.social.connect.google')
user_urls['/user/social/connect-vkontakte/'] = route('shiftuser.views_profile.ProfileSocialConnectVkontakte', 'user.social.connect.vkontakte')
user_urls['/user/social/connect-instagram/'] = route('shiftuser.views_profile.ProfileSocialConnectInstagram', 'user.social.connect.instagram')