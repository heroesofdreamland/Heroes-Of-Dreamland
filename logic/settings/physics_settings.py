from pymunk import Body

# Change both to KINEMATIC to disable physics (collision detection will still work)
player_body_type = Body.DYNAMIC
enemy_body_type = Body.DYNAMIC
max_unit_speed = 600
