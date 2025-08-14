import pygame
import random
import math

# --- 1. 初始化和常量设置 ---
pygame.init()

# 屏幕尺寸
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 颜色 (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 游戏设置
TARGET_RADIUS = 10  # 目标半径
TARGET_SPEED = 5    # 目标移动速度
GAME_DURATION = 30  # 游戏总时长（秒）

# --- 2. 创建游戏窗口和时钟 ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("跟枪练习程序 (Aim Trainer)")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36) # 用于显示文字的字体

# --- 3. 初始化游戏变量 ---
score = 0
# 将目标随机放置在屏幕中央区域
target_x = random.randint(TARGET_RADIUS, SCREEN_WIDTH - TARGET_RADIUS)
target_y = random.randint(TARGET_RADIUS, SCREEN_HEIGHT - TARGET_RADIUS)

# 随机化初始移动方向
target_dx = random.choice([-TARGET_SPEED, TARGET_SPEED])
target_dy = random.choice([-TARGET_SPEED, TARGET_SPEED])

start_time = pygame.time.get_ticks() # 获取游戏开始的时间戳
running = True

# --- 4. 主游戏循环 ---
while running:
    # --- 事件处理 ---
    for event in pygame.event.get():
        # 如果点击了窗口的关闭按钮
        if event.type == pygame.QUIT:
            running = False
            
        # 如果发生了鼠标点击事件
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 获取鼠标点击的坐标
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # 计算鼠标点击位置与目标中心的距离
            distance = math.sqrt((mouse_x - target_x)**2 + (mouse_y - target_y)**2)
            
            # 如果距离小于目标的半径，说明击中了
            if distance <= TARGET_RADIUS:
                score += 1
                # 击中后将目标立即重新随机放置，增加难度
                target_x = random.randint(TARGET_RADIUS, SCREEN_WIDTH - TARGET_RADIUS)
                target_y = random.randint(TARGET_RADIUS, SCREEN_HEIGHT - TARGET_RADIUS)
                # 随机化下一次移动方向
                target_dx = random.choice([-TARGET_SPEED, TARGET_SPEED])
                target_dy = random.choice([-TARGET_SPEED, TARGET_SPEED])

    # --- 游戏逻辑更新 ---
    
    # 移动目标
    target_x += target_dx
    target_y += target_dy

    # 边界碰撞检测
    # 如果碰到左右边缘，X方向速度反向
    if target_x <= TARGET_RADIUS or target_x >= SCREEN_WIDTH - TARGET_RADIUS:
        target_dx *= -1
    # 如果碰到上下边缘，Y方向速度反向
    if target_y <= TARGET_RADIUS or target_y >= SCREEN_HEIGHT - TARGET_RADIUS:
        target_dy *= -1
        
    # 计算剩余时间
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000 # 转换为秒
    #remaining_time = GAME_DURATION - elapsed_time
    remaining_time = 1
    # 如果时间结束，则停止游戏循环
    if remaining_time <= 0:
        running = False

    # --- 屏幕绘制 ---
    # 1. 填充背景色
    screen.fill(BLACK)
    
    # 2. 绘制目标
    pygame.draw.circle(screen, RED, (target_x, target_y), TARGET_RADIUS)

    # 3. 绘制分数
    score_text = font.render(f"得分 (Score): {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # 4. 绘制计时器
    timer_text = font.render(f"时间 (Time): {int(remaining_time)}", True, WHITE)
    screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))

    # --- 更新整个屏幕 ---
    pygame.display.flip()

    # 控制游戏帧率
    clock.tick(120) # 保持每秒120帧

# --- 5. 游戏结束界面 ---
# 游戏结束后，在屏幕中央显示最终得分
screen.fill(BLACK)
final_score_text = font.render(f"游戏结束! 最终得分: {score}", True, GREEN)
text_rect = final_score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
screen.blit(final_score_text, text_rect)
pygame.display.flip()

# 等待几秒或等待玩家关闭窗口
pygame.time.wait(5000) # 等待5秒

# 退出Pygame
pygame.quit()