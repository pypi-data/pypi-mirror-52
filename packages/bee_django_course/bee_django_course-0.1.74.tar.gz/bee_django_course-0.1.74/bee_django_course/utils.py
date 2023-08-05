# -*- coding: utf-8 -*-
__author__ = 'bee'

import urllib, urllib2, pytz, json
from django.http import HttpResponse
from django.db.models import Count, Sum, Max, Min
from django.db.models.functions import TruncMonth, TruncDay
from django.utils import timezone

import datetime
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import UserLive

LOCAL_TIMEZONE = pytz.timezone('Asia/Shanghai')


# =====http====
def http_get(url):
    f = urllib.urlopen(url)
    s = f.read()
    return s


def http_post(url, parameters=None):
    parameters = urllib.urlencode(parameters)
    request = urllib2.Request(url, parameters)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    res_data = urllib2.urlopen(request, timeout=10)
    res = res_data.read()
    return res


# ====dt====
# 获取本地当前时间
def get_now(tz=LOCAL_TIMEZONE):
    return timezone.now()


class JSONResponse(HttpResponse):
    def __init__(self, obj):
        if isinstance(obj, dict):
            _json_str = json.dumps(obj)
        else:
            _json_str = obj
        super(JSONResponse, self).__init__(_json_str, content_type="application/json;charset=utf-8")


def page_it(request, query_set, url_param_name='page', items_per_page=25):
    paginator = Paginator(query_set, items_per_page)

    page = request.GET.get(url_param_name)
    try:
        rs = paginator.page(page)
    except PageNotAnInteger:
        rs = paginator.page(1)
    except EmptyPage:
        rs = paginator.page(paginator.num_pages)

    return rs


# 获取用户姓名
def get_user_name(user):
    try:
        user_name = getattr(user, settings.USER_NAME_FIELD)
    except:
        user_name = user.username
    return user_name


# 返回直播分钟数，直播次数，直播天数
def get_user_live_data(user, start_dt=None, end_dt=None):
    vod_list = UserLive.objects.filter(status__in=[1, 2]).filter(user=user).filter(record_status=10)
    if start_dt:
        vod_list = vod_list.filter(start_time__gte=start_dt)
    if end_dt:
        vod_list = vod_list.filter(start_time__lt=end_dt)
    if vod_list.count() == 0:
        return 0, 0, 0
    res_mins = vod_list.aggregate(
        sum_duration=Sum('duration'))
    days_qurey_set = vod_list.annotate(day=TruncDay('start_time', tzinfo=LOCAL_TIMEZONE)).values('day') \
        .annotate(count=Count('id'), total=Sum('duration')).values('day', 'count', 'total') \
        .order_by('day')
    days_count = days_qurey_set.count()
    return res_mins["sum_duration"] / 60, vod_list.count(), days_count


# 某人是否可以观看视频，观看视频后是否能被记录为【助教已观看】。
# 条件1：有权限，条件2：录制本人，条件3：超过48小时。
def can_view_expired_live(user, user_live):
    # 本人可看，但不记入观看
    if user == user_live.user:
        return True, False

    # 判断是否助教
    is_mentor = user.is_user_assistant(user_live.user)

    # 设置过期时间
    if hasattr(settings, "COURSE_LIVE_EXPIRED_HOURS"):
        expired_dt = user_live.start_time + datetime.timedelta(hours=settings.COURSE_LIVE_EXPIRED_HOURS)
        # 未过期
        if timezone.now() < expired_dt:
            if is_mentor:
                return True, True
            else:
                return True, False
        # 已过期
        else:
            if user.has_perm('bee_django_course.view_expired_userlives'):
                return True, False
            else:
                return False, False
    # 未设置过期时间
    else:
        if is_mentor:
            return True, True
        else:
            return True, False
