# -*- coding: utf-8 -*-

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied

from django.views.static import serve
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.static import serve

from models import *

import os, json, string, random, datetime, re

def JsonResponse(data):
	return HttpResponse(json.dumps(data), content_type='application/json')

def views_static_serve(request, path):
 	return serve(request, path, os.path.join(os.path.dirname(__file__),'../static/'), False)

@csrf_exempt
def register_village(request):
	callback = ''
	try:
		callback = request.GET['callback']
		coord_x = request.GET['coord_x']
		coord_y = request.GET['coord_y']
		name = request.GET['name']
		last_wood = request.GET['scouted_wood']
		last_clay = request.GET['scouted_clay']
		last_iron = request.GET['scouted_iron']
		wood_level = request.GET['wood_level']
		clay_level = request.GET['clay_level']
		iron_level = request.GET['iron_level']
		wall_level = request.GET['wall_level']
		last_modified = datetime.datetime.strptime(request.GET['reported_time'], '%b %d, %Y %H:%M:%S') + datetime.timedelta(hours=8)
	except:
		return HttpResponse('error')

	village, _ = Village.objects.get_or_create(coord_x=coord_x, coord_y=coord_y)
	if village.last_modified > last_modified:
		return HttpResponse('%s(%s)' % (callback, json.dumps({'msg': 'skip'})))
	village.last_modified = last_modified
	village.last_wood = last_wood
	village.last_clay = last_clay
	village.last_iron = last_iron
	if wood_level >= 0:
		village.wood_level = wood_level
		village.clay_level = clay_level
		village.iron_level = iron_level
		village.wall_level = wall_level
	village.name = name
	village.save()

	return HttpResponse('%s(%s)' % (callback, json.dumps({'msg': 'success'})))

@csrf_exempt
def get_next_village(request):
	callback = ''
	try:
		callback = request.GET['callback']
		my_x = int(request.GET['my_x'])
		my_y = int(request.GET['my_y'])
		min_res = int(request.GET['min_res'])
		on_ride = request.GET['on_ride'].strip()
		if on_ride[0] != '[' or on_ride[-1] != ']':
			return HttpResponse('error')
		on_ride = set(eval(on_ride))
	except:
		return HttpResponse('error')

	vills = Village.objects.all()
	arr = []
	for vill in vills:
		res = vill.now_wood + vill.now_clay + vill.now_iron
		if res < min_res or ((vill.coord_x, vill.coord_y) in on_ride):
			continue
		dist = (my_x - vill.coord_x) ** 2 + (my_y - vill.coord_y) ** 2
		arr.append((dist, vill))
	if not arr:
		return HttpResponse('%s(%s)' % (callback, json.dumps({'msg': 'empty'})))
	arr.sort()
	vill = arr[0][1]
	dist = arr[0][0] ** 0.5
	res = vill.now_wood + vill.now_clay + vill.now_iron + int(dist * 10 / 60 * (vill.wood_per_hour + vill.clay_per_hour + vill.iron_per_hour))
	cnt = res / 80

	return HttpResponse('%s(%s)' % (callback, json.dumps({'msg': 'success', 'x': vill.coord_x, 'y': vill.coord_y, 'cnt': cnt})))
