# utils.py

import supabase
from django.conf import settings

def initialize_supabase():
    return supabase.create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)



supabase_client = initialize_supabase()
