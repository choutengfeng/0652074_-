"""The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameInstruction, GameStatus, PlatformAction
)

def ml_loop():
    """The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.

    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()

    ball_postition_history=[]
    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()
        platform_center_x=scene_info.platform[0]+4
        ball_postition_history.append(scene_info.ball)
        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            print( "end" ,end='\n')
            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue
        
        if(len(ball_postition_history) > 1):
            vx=ball_postition_history[-1][0]-ball_postition_history[-2][0]
            vy=ball_postition_history[-1][1]-ball_postition_history[-2][1]

            if vy > 0 :
                print("down" ,end='\n')
                down=1
                final_x =ball_postition_history[-1][0] + (((400-ball_postition_history[-1][1])/vy)*vx)
                if final_x < 0:
                    final_x = 0 - final_x 
                elif final_x>200 :
                    final_x = 400 - final_x 
            else:
                print("up" ,end='\n')
                down=0
                
            print( "ball_x=",ball_postition_history[-1][0] ,end='\n')
            print( "ball_y=",ball_postition_history[-1][1] ,end='\n')
            print( "vx=",vx ,end='\n')
            print( "vy=",vy ,end='\n')
            print( "finial_X" ,final_x ,end='\n')
            print( end='\n')
            
            # 3.3. Put the code here to handle the scene information
            if  platform_center_x >  final_x:
            # 3.4. Send the instruction for this frame to the game process
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            if  platform_center_x <  final_x:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)    
