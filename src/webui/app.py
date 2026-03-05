# -*- coding: utf-8 -*-
"""
抽卡模拟器 Web GUI
使用 Flask 提供 Web 界面
支持角色池和武器池切换
"""

from flask import Flask, render_template, jsonify, request
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gacha_simulator import (
    CharacterPool,
    WeaponPool,
    create_standard_character_pool,
    create_standard_weapon_pool,
    PoolConfigManager
)

app = Flask(__name__)

# 全局池子实例
pools = {
    'character': None,
    'weapon': None
}

# 当前选中的池子
current_pool_type = 'character'


def get_current_pool():
    """获取当前池子，如果不存在则创建"""
    if pools[current_pool_type] is None:
        if current_pool_type == 'character':
            pools[current_pool_type] = create_standard_character_pool()
        else:
            pools[current_pool_type] = create_standard_weapon_pool()
    return pools[current_pool_type]


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/pool/switch', methods=['POST'])
def api_switch_pool():
    """切换池子"""
    global current_pool_type
    data = request.get_json()
    pool_type = data.get('pool_type', 'character')
    
    if pool_type not in ['character', 'weapon']:
        return jsonify({
            'success': False,
            'message': '无效的池子类型'
        }), 400
    
    current_pool_type = pool_type
    pool = get_current_pool()
    
    return jsonify({
        'success': True,
        'pool_type': current_pool_type,
        'pool_info': pool.get_pool_info(),
        'statistics': pool.get_statistics()
    })


@app.route('/api/pool/info', methods=['GET'])
def api_pool_info():
    """获取当前池子信息"""
    pool = get_current_pool()
    
    return jsonify({
        'success': True,
        'pool_type': current_pool_type,
        'pool_info': pool.get_pool_info(),
        'statistics': pool.get_statistics()
    })


@app.route('/api/single_draw', methods=['POST'])
def api_single_draw():
    """单次抽卡API"""
    pool = get_current_pool()
    result = pool.single_draw()
    stats = pool.get_statistics()
    
    response_data = {
        'success': True,
        'pool_type': current_pool_type,
        'result': {
            'rarity': result.rarity,
            'is_rate_up': result.is_rate_up,
            'is_top_rarity': result.is_top_rarity,
            'reward': result.reward
        },
        'total_draws': pool.total_draws,
        'total_rewards': pool.total_rewards,
        'statistics': stats,
        'history': [
            {
                'rarity': r.rarity,
                'is_rate_up': r.is_rate_up,
                'is_top_rarity': r.is_top_rarity,
                'reward': r.reward
            } 
            for r in pool.draw_history[-10:]
        ]
    }
    
    # 武器池额外返回命定值信息
    if current_pool_type == 'weapon' and hasattr(pool, 'fate_points'):
        response_data['fate_points'] = pool.fate_points
    
    return jsonify(response_data)


@app.route('/api/multi_draw', methods=['POST'])
def api_multi_draw():
    """多连抽API"""
    pool = get_current_pool()
    data = request.get_json() or {}
    count = data.get('count', 10)
    
    # 限制单次最多抽100次（避免界面卡顿）
    count = min(count, 100)
    
    results = pool.multi_draw(count)
    stats = pool.get_statistics()
    
    response_data = {
        'success': True,
        'pool_type': current_pool_type,
        'results': [
            {
                'rarity': r.rarity,
                'is_rate_up': r.is_rate_up,
                'is_top_rarity': r.is_top_rarity,
                'reward': r.reward
            } 
            for r in results
        ],
        'total_draws': pool.total_draws,
        'total_rewards': pool.total_rewards,
        'statistics': stats,
        'history': [
            {
                'rarity': r.rarity,
                'is_rate_up': r.is_rate_up,
                'is_top_rarity': r.is_top_rarity,
                'reward': r.reward
            } 
            for r in pool.draw_history[-50:]
        ]
    }
    
    # 武器池额外返回命定值信息
    if current_pool_type == 'weapon' and hasattr(pool, 'fate_points'):
        response_data['fate_points'] = pool.fate_points
    
    return jsonify(response_data)


@app.route('/api/simulate', methods=['POST'])
def api_simulate():
    """大规模模拟API"""
    pool = get_current_pool()
    data = request.get_json()
    count = data.get('count', 100000)
    
    # 限制最大模拟次数为1000万
    count = min(count, 10000000)
    
    # 执行模拟
    results = pool.multi_draw(count)
    stats = pool.get_statistics()
    
    # 计算理论统计值
    theoretical_stats = pool.calculate_theoretical_stats()
    
    # 计算经验统计值
    empirical_stats = pool.calculate_empirical_stats()
    
    response_data = {
        'success': True,
        'pool_type': current_pool_type,
        'simulated_count': count,
        'total_draws': pool.total_draws,
        'total_rewards': pool.total_rewards,
        'statistics': stats,
        'theoretical_stats': theoretical_stats,
        'empirical_stats': empirical_stats
    }
    
    # 武器池额外返回命定值信息
    if current_pool_type == 'weapon' and hasattr(pool, 'fate_points'):
        response_data['fate_points'] = pool.fate_points
    
    return jsonify(response_data)


@app.route('/api/statistics', methods=['GET'])
def api_statistics():
    """获取统计信息API"""
    pool = get_current_pool()
    stats = pool.get_statistics()
    
    response_data = {
        'success': True,
        'pool_type': current_pool_type,
        'total_draws': pool.total_draws,
        'total_rewards': pool.total_rewards,
        'statistics': stats,
        'history': [
            {
                'rarity': r.rarity,
                'is_rate_up': r.is_rate_up,
                'is_top_rarity': r.is_top_rarity,
                'reward': r.reward
            } 
            for r in pool.draw_history[-100:]
        ]
    }
    
    # 武器池额外返回命定值信息
    if current_pool_type == 'weapon' and hasattr(pool, 'fate_points'):
        response_data['fate_points'] = pool.fate_points
    
    return jsonify(response_data)


@app.route('/api/reset', methods=['POST'])
def api_reset():
    """重置统计API"""
    pool = get_current_pool()
    pool.reset_statistics()
    
    return jsonify({
        'success': True,
        'pool_type': current_pool_type,
        'message': '统计已重置'
    })


@app.route('/api/config', methods=['GET'])
def api_get_config():
    """获取配置"""
    pool = get_current_pool()
    
    return jsonify({
        'success': True,
        'pool_type': current_pool_type,
        'config': pool.config,
        'pool_info': pool.get_pool_info()
    })


@app.route('/api/config', methods=['POST'])
def api_update_config():
    """更新配置并重新创建池子"""
    global pools
    data = request.get_json()
    pool_type = data.get('pool_type', current_pool_type)
    config = data.get('config', {})
    
    try:
        # 创建新的池子实例
        if pool_type == 'character':
            pools['character'] = CharacterPool(config, use_custom_config=True)
        else:
            pools['weapon'] = WeaponPool(config, use_custom_config=True)
        
        return jsonify({
            'success': True,
            'pool_type': pool_type,
            'message': '配置已更新',
            'pool_info': pools[pool_type].get_pool_info()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'配置更新失败: {str(e)}'
        }), 400


@app.route('/api/pools/list', methods=['GET'])
def api_list_pools():
    """列出所有可用的池子配置"""
    configs = {
        'character': {
            'standard': PoolConfigManager.get_config('character'),
            'limited': PoolConfigManager.get_config('limited_character'),
            'novice': PoolConfigManager.get_config('novice'),
        },
        'weapon': {
            'standard': PoolConfigManager.get_config('weapon'),
        }
    }
    
    return jsonify({
        'success': True,
        'configs': configs
    })


def run_server(host='0.0.0.0', port=5000, debug=True):
    """启动服务器"""
    print("=" * 60)
    print("抽卡模拟器 Web GUI".center(60))
    print("=" * 60)
    print(f"服务器启动中...")
    print(f"请在浏览器中访问: http://localhost:{port}")
    print(f"当前支持的池子：")
    print(f"  - 角色池（标准/限定/新手）")
    print(f"  - 武器池（标准，命定值机制）")
    print(f"按 Ctrl+C 停止服务器")
    print("=" * 60)
    
    app.run(debug=debug, host=host, port=port)


if __name__ == '__main__':
    run_server()
