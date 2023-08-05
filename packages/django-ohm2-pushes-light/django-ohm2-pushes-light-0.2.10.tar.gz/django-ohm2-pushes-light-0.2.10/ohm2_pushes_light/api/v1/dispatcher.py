from ohm2_handlers_light import utils as h_utils
from ohm2_pushes_light.decorators import ohm2_pushes_light_safe_request
from ohm2_pushes_light import utils as ohm2_pushes_light_utils
from ohm2_pushes_light import settings
from . import errors as api_v1_errors
from . import settings as api_v1_settings



@ohm2_pushes_light_safe_request
def gateways_onesignal_register_device(request, params, **pipeline_options):
	p = h_utils.cleaned(params, (
							("string", "player_id", 1),
							("string", "push_token", 1),
							("integer", "platform", None),
						))

	platform, player_id, push_token = p["platform"], p["player_id"], p["push_token"]

	device = ohm2_pushes_light_utils.onesignal_utils.filter_device(player_id = player_id).first()
	if device:
		device = ohm2_pushes_light_utils.onesignal_utils.update_device(
			device,
			user = request.user,
			platform = platform,
			push_token = push_token,
		)
	else:
		device = ohm2_pushes_light_utils.onesignal_utils.create_device(request.user, platform, player_id, push_token)
	
	
	res = {
		"error" : None,
		"ret" : True,
	}
	return res




