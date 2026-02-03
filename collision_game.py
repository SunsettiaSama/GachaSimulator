import pygame
import random
import sys

# 初始化
pygame.init()
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge Game - Press ESC to Exit")
clock = pygame.time.Clock()

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
BLUE = (50, 150, 255)
GREEN = (50, 255, 150)
YELLOW = (255, 220, 50)

# 玩家
player = {
    'x': WIDTH // 2 - 25,
    'y': HEIGHT - 80,
    'width': 50,
    'height': 50,
    'speed': 7,
    'color': BLUE
}

# 障碍物列表
obstacles = []
obstacle_timer = 0
obstacle_interval = 60  # 帧数

# 游戏状态
score = 0
game_over = False

# 使用支持中文的字体
try:
    # Windows系统字体路径
    font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 28)  # 微软雅黑
    big_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 60)
except:
    try:
        font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 28)  # 黑体
        big_font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 60)
    except:
        # 如果找不到中文字体，使用英文
        font = pygame.font.Font(None, 36)
        big_font = pygame.font.Font(None, 72)
        print("警告: 未找到中文字体，使用英文显示")

def create_obstacle():
    """创建新障碍物"""
    return {
        'x': random.randint(0, WIDTH - 40),
        'y': -40,
        'width': random.randint(30, 70),
        'height': random.randint(30, 70),
        'speed': random.randint(3, 8),
        'color': random.choice([RED, YELLOW, GREEN])
    }

def check_collision(player, obstacle):
    """检测碰撞"""
    return (player['x'] < obstacle['x'] + obstacle['width'] and
            player['x'] + player['width'] > obstacle['x'] and
            player['y'] < obstacle['y'] + obstacle['height'] and
            player['y'] + player['height'] > obstacle['y'])

def draw_rect(obj):
    """绘制矩形对象"""
    pygame.draw.rect(screen, obj['color'], 
                     (obj['x'], obj['y'], obj['width'], obj['height']))
    pygame.draw.rect(screen, WHITE, 
                     (obj['x'], obj['y'], obj['width'], obj['height']), 2)

# 游戏主循环
running = True
while running:
    clock.tick(60)
    
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE and game_over:
                # 重置游戏
                game_over = False
                score = 0
                obstacles.clear()
                player['x'] = WIDTH // 2 - 25
    
    if not game_over:
        # 玩家移动
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player['x'] -= player['speed']
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player['x'] += player['speed']
        
        # 限制玩家在屏幕内
        player['x'] = max(0, min(WIDTH - player['width'], player['x']))
        
        # 创建障碍物
        obstacle_timer += 1
        if obstacle_timer >= obstacle_interval:
            obstacles.append(create_obstacle())
            obstacle_timer = 0
            # 难度递增
            obstacle_interval = max(30, obstacle_interval - 1)
        
        # 更新障碍物
        for obs in obstacles[:]:
            obs['y'] += obs['speed']
            
            # 检测碰撞
            if check_collision(player, obs):
                game_over = True
            
            # 移除屏幕外的障碍物并加分
            if obs['y'] > HEIGHT:
                obstacles.remove(obs)
                score += 10
    
    # 绘制
    screen.fill(BLACK)
    
    if not game_over:
        # 绘制玩家
        draw_rect(player)
        
        # 绘制障碍物
        for obs in obstacles:
            draw_rect(obs)
        
        # 显示分数
        score_text = font.render(f'分数: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))
    else:
        # 游戏结束画面
        game_over_text = big_font.render('游戏结束!', True, RED)
        score_text = font.render(f'最终分数: {score}', True, WHITE)
        restart_text = font.render('按空格键重新开始', True, GREEN)
        
        screen.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2 - 100))
        screen.blit(score_text, (WIDTH//2 - 100, HEIGHT//2))
        screen.blit(restart_text, (WIDTH//2 - 150, HEIGHT//2 + 60))
    
    pygame.display.flip()

pygame.quit()
sys.exit()
