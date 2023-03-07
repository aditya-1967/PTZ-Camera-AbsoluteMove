def check_camera_idle():
	myCam = ONVIFCamera(IP, PORT, USER, PASS)
	media_service = myCam.create_media_service()
	profile = media_service.GetProfiles()[0]

	ptz_service = myCam.create_ptz_service()

	# checking if camera supports PTZ
	if not ptz_service:
		print('PTZ not supported by camera')
	else:
		print('PTZ supported by camera')

	status = ptz_service.GetStatus({'ProfileToken': profile.token})

	# checking if PTZ functionality is active or not
	if status.Position and status.Position.PanTilt:
		print("PTZ functionality is active")
	else:
		print("PTZ functionality is inactive")

	# checking if PTZ camera is in moving state or not
	if status.Position and status.Position.PanTilt and (status.MoveStatus['PanTilt'] == 'IDLE' or status.MoveStatus['Zoom'] == 'IDLE'):
		print('PTZ is not in moving state')
	else:
		print('PTZ is in moving state')