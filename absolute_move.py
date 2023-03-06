def move_up(ptz, request, move):
    print(request.Position.PanTilt.x, request.Position.PanTilt.y)
    
    if YNOW + move >= 1.0:
        request.Position.PanTilt.y = YNOW + (1.0 - YNOW)
        print('Reached maximum limit')
    else:
        request.Position.PanTilt.y = YNOW + move
    
    print(request.Position.PanTilt.x, request.Position.PanTilt.y)
    
    perform_move(ptz, request)


def moving_up(step):
    move = step
    setup()
    get_status()
    move_up(ptz, positionrequest, move)
    
    
def move_down(ptz, request, move):
    print(request.Position.PanTilt.x, request.Position.PanTilt.y)
    if YNOW - move <= -1:
        request.Position.PanTilt.y = YNOW + (-1.0 + YNOW)
        print('Reached maximum limit')
    else:
        request.Position.PanTilt.y = YNOW - move
    
    print(request.Position.PanTilt.x, request.Position.PanTilt.y)
    
    perform_move(ptz, request)

    
def moving_down(step):
    move = step
    setup()
    get_status()
    move_down(ptz, positionrequest, move)

    
def move_left(ptz, request, move):
    print(request.Position.PanTilt.x, request.Position.PanTilt.y)
    if XNOW - move >= -0.99:
        request.Position.PanTilt.x = XNOW - move
    elif abs(XNOW + move) >= 0.0:
        request.Position.PanTilt.x = abs(XNOW) - move
    elif abs(XNOW) <= 0.01:
        request.Position.Pantilt.x = XNOW
    
    request.Position.PanTilt.y = YNOW
    print(request.Position.PanTilt.x, request.Position.PanTilt.y)
    perform_move(ptz, request)
    

def moving_left(step):
    move = step
    setup()
    get_status()
    move_left(ptz, positionrequest, move)
    

def move_right(ptz, request, move):
    print(request.Position.PanTilt.x, request.Position.PanTilt.y)
    if XNOW + move <= 1.0:
        request.Position.PanTilt.x = XNOW + move
    elif XNOW <= 1.0 and XNOW > 0.99:
        request.Position.PanTilt.x = -XNOW
    elif XNOW < 0:
        request.Position.PanTilt.x = XNOW + move
    elif XNOW <= 0.105556 and XNOW >- 0.11:
        request.Position.PanTilt.x = XNOW
    
    request.Position.PanTilt.y = YNOW
    print(request.Position.PanTilt.x, request.Position.PanTilt.y)
    perform_move(ptz, request)


def moving_right(step):
    move = step
    setup()
    get_status()
    move_right(ptz, positionrequest, move)


def zoom_in(ptz, request, move):
    print(request.Position.Zoom.x)
    
    if Zoom + Move >= 1.0:
        request.Position.Zoom = 1.0
        print("Maximum Zoom Limit Reached")
    else:
        request.Position.Zoom = Zoom + Move
        print("Zooming in ...")
    
    print(request.Position.Zoom)
    perform_move(ptz, request)
    

def zooming_in(step):
    move = step
    setup()
    get_status()
    zoom_in(ptz, positionrequest, move)
    

def zoom_out(ptz, request, move):
    print(request.Position.Zoom.x)
    
    if Zoom - Move <= 0.0:
        request.Position.Zoom = 0.0
        print("Minimum Zoom Limit Reached")
    else:
        request.Position.Zoom = Zoom - Move
        print("Zooming Out ...")
    
    perform_move(ptz, request)
    print(request.Position.Zoom)
    

def zooming_out(step):
    move = step
    setup()
    get_status()
    zoom_out(ptz, positionrequest, move)