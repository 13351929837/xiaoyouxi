'''

    ## 分析
        1.在屏幕下方中央生成一个炮台
        2.随机生成蝙蝠并作四周反弹运动
        3.时时捕获鼠标位置，调整炮台角度
        4.鼠标点击射出炮弹
            ①.判断是否射中
            ②.射中则分数增加

'''
import pygame,math,random

# 定义炮台转动函数
def whirl(image,a,b):
    mouse_x,mouse_y = pygame.mouse.get_pos()
    angle = math.degrees(math.atan2(mouse_x-400,600-mouse_y)) #弧度转角度
    new_image = pygame.transform.rotate(image,-angle)
    screen.blit(new_image,(a,b))

# 定义蝙蝠随机运动函数
def batmove(direction,n):
    global new_x,new_y
    if direction==1:
        new_x=locations[n][0]+speedx[n]
        new_y=locations[n][1]+speedy[n]
    elif direction==2:
        new_x=locations[n][0]+speedx[n]
        new_y=locations[n][1]-speedy[n]
    elif direction==3:
        new_x=locations[n][0]-speedx[n]
        new_y=locations[n][1]+speedy[n]
    else:
        new_x=locations[n][0]-speedx[n]
        new_y=locations[n][1]-speedy[n]
    return (new_x,new_y)

# 初始化
pygame.init()
flag = False    #判断鼠标按下条件
count_shell = 10
count_score = 0
font = pygame.font.SysFont("Arial", 24)
screen = pygame.display.set_mode([800,600])
keep_going = True
White = (255,255,255)
Black = (0,0,0)

# 更改程序名称
pygame.display.set_caption("Sharpshooter")

# 加载背景图片
background = pygame.image.load("Background.jpg")

# 加载炮台和蝙蝠
cannon = pygame.image.load("Cannon.png")
bat = pygame.image.load("Bat.jpg")
shell = pygame.image.load("shell.png")
colorkey = bat.get_at((0,0))
bat.set_colorkey(colorkey)

# 随机蝙蝠位置和运动方向
locations = [0]*10  #蝙蝠（x，y）位置存放
direction = [0]*10  #随机方向
speedx = [5]*10  #调整方向
speedy = [5]*10
bat_flag = [1]*10  #蝙蝠是否被击中标记
bat_rect = bat.get_rect()   #获取蝙蝠位置
# 炮弹初始化
shell_x = 400
shell_y = 500
shell_angle = 0
shell_xy = (400,500)
shell_rect = shell.get_rect()   #获取炮弹位置

# 初始化随机蝙蝠位置和方向
for n in range(10):
    locations[n] = (random.randint(200,700),random.randint(100,350))
    direction[n] = int(random.randint(1,4))

timer=pygame.time.Clock()  #时钟


while keep_going :
    # 判断游戏是否结束
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_going = False
    
    # 鼠标左键记录炮弹方位
    if event.type == pygame.MOUSEBUTTONDOWN:
        if pygame.mouse.get_pressed()[0]:  
            flag = True
        mouse_x,mouse_y = pygame.mouse.get_pos()
        shell_angle = math.atan2(mouse_x-400,600-mouse_y)

    '''
    # 加载背景图
    screen.blit(background,(0,0))
    '''

    # 绘制炮弹
    if flag:    
        new_shell = pygame.transform.rotate(shell,-math.degrees(shell_angle))
        screen.blit(new_shell,shell_xy)
        shell_x += 5*math.sin(shell_angle)
        shell_y -= 5*math.cos(shell_angle)
        shell_xy = (shell_x,shell_y)
        shell_rect[0] = shell_x - shell.get_width()/2  #修改炮弹位置
        shell_rect[1] = shell_y - shell.get_height()/2  
        
        # 判断炮弹是否越界，越界则炮弹消失
        if shell_x<=0 or shell_x+shell.get_width()>=800:
            shell_x,shell_y = 400,500
            shell_xy = (shell_x,shell_y)
            flag = False
            count_shell -= 1
        if shell_y <= 0 :
            shell_x,shell_y = 400,500
            shell_xy = (shell_x,shell_y)
            flag = False    
            count_shell -= 1


    # 绘制蝙蝠
    for n in range(10): 
        if bat_flag[n]: 
            screen.blit(bat,batmove(direction[n],n))
            
            # 判断蝙蝠是否越界，越界则更改方向
            if new_x <= 200 or new_x + bat.get_width() >= 800:
                speedx[n] = -speedx[n]
            if new_y <= 0 or new_y+bat.get_height() >= 450:
                speedy[n] = -speedy[n]

            locations[n] = (new_x,new_y)


    # 碰撞判定
    for n in range(10):
        if pygame.Rect.colliderect(shell_rect,locations[n][0]-bat.get_width()/2,
            locations[n][1]-bat.get_height()/2,bat.get_width(),bat.get_height()):
            flag = False
            bat_flag[n]=0
            locations[n]=(800,600)
            shell_x,shell_y = 400,500
            shell_xy = (shell_x,shell_y)
            shell_rect = shell.get_rect()
            count_shell -= 1
            count_score += 10


    # 实时获取鼠标位置以改变炮台方向
    whirl(cannon,350,465)

    # 显示分数以及炮弹剩余
    draw_string = "Your score:   " + str(count_score)
    draw_string += "  -  Remaining shells : " + str(count_shell)
    text = font.render(draw_string, True, Black)
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = 10
    screen.blit (text, text_rect)

    # 游戏结束判定
    if count_shell == 0:
        if count_score == 100:
            print(f"Поздравляю с убийством {int(count_score/10)} летучих мышей，Вы - чемпион по стрельбе!!!")
        elif count_score>=5 :
            print(f"Поздравляю с убийством {int(count_score/10)} летучих мышей，приближаясь к совершенству!!")
        elif count_score>=1 :
            print(f"Поздравляю с убийством {int(count_score/10)} летучих мышей，Ты молодец!")
        else :
            print("Вы не убили ни одной летучей мыши. Продолжайте в том же духе!")
        pygame.quit()
        exit()
    
    # 更新画布
    pygame.display.update()
    screen.fill(White)
    timer.tick(40)  #每秒40

pygame.quit()

