from django.test import TestCase
from django.urls import reverse
from heyurl.utils import cross_helper


def test_create_random_key(self):
    rnd_key = cross_helper._create_random_key()
    ok_key = True
    for char in rnd_key:
        if char not in cross_helper.chars:
            ok_key = False
            break
    self.assertTrue(len(rnd_key) <= cross_helper.max_length_key and ok_key  )

