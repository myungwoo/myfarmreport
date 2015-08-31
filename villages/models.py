# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User, Group

import datetime

_per_hour = [5, 30, 35, 41, 47, 55, 64, 74, 86, 100, 117, 136, 158, 184, 214, 249, 289, 337, 391, 455, 530, 616, 717, 833, 969, 1127, 1311, 1525, 1774, 2063, 2400]

class Village(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, default=None)
	name = models.CharField(default='none', max_length=40)
	coord_x = models.IntegerField()
	coord_y = models.IntegerField()
	last_wood = models.IntegerField(default=0)
	last_clay = models.IntegerField(default=0)
	last_iron = models.IntegerField(default=0)
	wood_level = models.IntegerField(default=0)
	clay_level = models.IntegerField(default=0)
	iron_level = models.IntegerField(default=0)
	wall_level = models.IntegerField(default=0)
	last_modified = models.DateTimeField(default=datetime.datetime(1900, 1, 1))

	@property
	def wood_per_hour(self):
		return _per_hour[self.wood_level]

	@property
	def clay_per_hour(self):
		return _per_hour[self.clay_level]

	@property
	def iron_per_hour(self):
		return _per_hour[self.iron_level]

	@property
	def time_in_hour(self):
		return (datetime.datetime.now() - self.last_modified).seconds / 3600.

	@property
	def now_wood(self):
		return int(self.last_wood + self.time_in_hour * self.wood_per_hour)
	@property
	def now_clay(self):
		return int(self.last_clay + self.time_in_hour * self.clay_per_hour)
	@property
	def now_iron(self):
		return int(self.last_iron + self.time_in_hour * self.iron_per_hour)

	def __unicode__(self):
		return u'''[%d|%d] %s (%d, %d, %d)'''%(self.coord_x, self.coord_y, self.name, self.now_wood, self.now_clay, self.now_iron)
