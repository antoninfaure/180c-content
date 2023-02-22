from os import path
import os 
import json

def print_err(msg):
    print('\033[91m' + msg + '\033[0m')
    
def print_ignore(msg):
    print('\033[93m' + msg + '\033[0m')

def check_place(code, data):
    result = {
        'code': code
    }
    f = open(path.join('.', 'crieur', 'config_crieur.json'), "r", encoding='utf8')
    config_crieur = json.load(f)

    if 'name' not in data or not data['name']: raise Exception("Missing name")
    result['name'] = data['name']

    if 'available' not in data or 'available' not in data : raise Exception("Missing available")
    result['available'] = data['available']

    if 'style' not in data or not data['style'] : raise Exception("Missing style")
    result['style'] = data['style']

    if 'front' in data and data['front']:
        if (not path.exists(path.join('.', 'crieur', code, 'images', data['front']))):
            print_ignore(f"[{code}] error: {data['front']} file doesn't exists, solution: front ignored")
        else : result['front'] = f'crieur/{code}/{data["front"]}'

    if 'banner' in data and data['banner']:
        if (not path.exists(path.join('.', 'crieur', code, 'images', data['banner']))):
            print_ignore(f"[{code}] error: {data['banner']} file doesn't exists, solution: banner ignored")
        else: result['banner'] = f'crieur/{code}/{data["banner"]}'

    if 'types' not in data or not data['types'] : raise Exception("Missing types")
    allowed_types = list(map(lambda x: x['code'], config_crieur['types']))
    for place_type in data['types']:
        if (place_type not in allowed_types):
            raise Exception(f"Wrong type ({place_type})")
    result['types'] = data['types']

    if 'tags' in data and data['tags']:
        place_tags = []
        allowed_tags = list(map(lambda x: x['code'], config_crieur['tags']))
        for tag in data['tags']:
            if (tag not in allowed_tags):
                print_ignore(f"[{code}] error: Wrong tag {tag}, solution: tag ignored")
                continue
            place_tags.append(tag)
        result['tags'] = place_tags
    
    if 'description' not in data or not data['description'] : raise Exception("Missing description")
    result['description'] = data['description']

    if 'tips' in data and data['tips'] : result['tips'] = data['tips']

    if 'price' not in data or not data['price'] : raise Exception("Missing price")
    result['price'] = data['price']
    
    if not data['priceTag'] : raise Exception("Missing priceTag")
    if not isinstance(data['priceTag'], int): raise Exception("priceTag not int")
    if data['priceTag'] not in config_crieur['priceTags']: raise Exception("priceTag out of range")
    result['priceTag'] = data['priceTag']

    if data['links']:
        allowed_socials = list(map(lambda x: x['social'], config_crieur['links']))
        place_links = []
        for link in data['links']:
            if (link['social'] not in allowed_socials):
                print_ignore(f"[{code}] error: Wrong social {link['social']}, solution: link ignored")
                continue
            if ('url' not in link):
                print_ignore(f"[{code}] error: Missing link url {link['social']}, solution: link ignored")
                continue
            place_links.append(link)
        result['links'] = place_links

    if 'tops' in data and data['tops']:
        place_tops = []
        for top in data['tops']:
            if (not 'name' in top):
                print_ignore(f"[{code}] error: Missing top name, solution: top ignored")
                continue
            if ('photo' in top):
                valid_top_photo = True
                if (not path.exists(path.join('.', 'crieur', code, 'images', top['photo']))):
                    print_ignore(f"[{code}] error: {top['photo']} file doesn't exists, solution: top photo ignored")
                    valid_top_photo = False
                if (valid_top_photo == True):
                    top['photo'] = f'crieur/{code}/{top["photo"]}'
                else : del top['photo']
            place_tops.append(top)
        result['tops'] = place_tops
    
    if 'locations' in data and data['locations']:
        place_locations = []
        for location in data['locations']:
            if ('latitude' not in location):
                print_ignore(f"[{code}] error: Missing location latitude, solution: location ignored")
                continue
            if ('longitude' not in location):
                print_ignore(f"[{code}] error: Missing location longitude, solution: location ignored")
                continue
            if ('map' not in location):
                print_ignore(f"[{code}] error: Missing location map, solution: location ignored")
                continue
            if ('horaires' not in location):
                print_err(f"[{code}] error: Missing location horaires, solution: location ignored")
                continue
            valid_days = True
            for horaire in location['horaires']:
                if (horaire['name'] not in ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]):
                    print_ignore(f"[{code}] error: Wrong day in location horaires ({horaire['name']}), solution: location ignored")
                    valid_days = False
            if (valid_days == False): continue
            place_locations.append(location)
        result['locations'] = place_locations

    return result