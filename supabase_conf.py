from supabase import create_client, Client
from constants import SUPABASE_URL, SUPABASE_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_location(user_id):
    response = supabase.table('users').select('lat', 'lon').eq('id', user_id).execute()
    lat = round(float(response.data[0]['lat']), ndigits=2)
    lon = round(float(response.data[0]['lon']), ndigits=2)
    return lat, lon


def set_location(user_id, lat, lon):
    existing_user = supabase.table('users').select('*').eq('id', user_id).execute().data
    if len(existing_user) <= 0:
        supabase.table('users').insert({"id": user_id, 'lat': lat, 'lon': lon}).execute()
    else:
        supabase.table('users').update({'lat': lat, 'lon': lon}).eq("id", user_id).execute()
