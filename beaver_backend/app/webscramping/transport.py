dict_region = {
    'Graças': {
        'bus_average': 194.7, 
        'uber': 1144.00,
        'http_response': {
            'message': 'The request has succeeded.', 
            'code': 200
        }
    },
    'Várzea': {
        'bus_average': 194.7, 
        'uber': 1264.56,
        'http_response': {
            'message': 'The request has succeeded.', 
            'code': 200
        }
    }, 
    'Boa Viagem': {
        'bus_average': 192.13, 
        'uber': 1172.16,
        'http_response': {
            'message': 'The request has succeeded.', 
            'code': 200
        }
    }
}
def get_transport_data(region): 
  if not region:
    return {}
  if region in dict_region:
    return dict_region[region]
  else:
    return {}