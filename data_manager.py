import json
import os
import pandas as pd
from typing import Dict, List, Any
from datetime import datetime
import io

class DataManager:
    def __init__(self):
        self.contestants_file = "contestants.json"
        self.scores_file = "scores.json"
        
    def load_contestants(self) -> List[Dict]:
        """加载选手信息"""
        if os.path.exists(self.contestants_file):
            try:
                with open(self.contestants_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_contestants(self, contestants: List[Dict]) -> bool:
        """保存选手信息"""
        try:
            with open(self.contestants_file, 'w', encoding='utf-8') as f:
                json.dump(contestants, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False
    
    def load_scores(self) -> Dict:
        """加载评分信息"""
        if os.path.exists(self.scores_file):
            try:
                with open(self.scores_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_scores(self, scores: Dict) -> bool:
        """保存评分信息"""
        try:
            with open(self.scores_file, 'w', encoding='utf-8') as f:
                json.dump(scores, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False
    
    def calculate_final_score(self, scores: List[float]) -> float:
        """计算最终得分：去掉最高分和最低分后的平均分"""
        if len(scores) < 3:
            return 0.0
        
        sorted_scores = sorted(scores)
        # 去掉最高分和最低分
        trimmed_scores = sorted_scores[1:-1]
        return sum(trimmed_scores) / len(trimmed_scores)
    
    def get_rankings(self) -> List[Dict]:
        """获取选手排名"""
        contestants = self.load_contestants()
        scores_data = self.load_scores()
        
        rankings = []
        for contestant in contestants:
            contestant_id = str(contestant['id'])
            if contestant_id in scores_data:
                scores = scores_data[contestant_id]
                final_score = self.calculate_final_score(scores)
                rankings.append({
                    'id': contestant['id'],
                    'name': contestant['name'],
                    'gender': contestant.get('gender', ''),
                    'age': contestant.get('age', ''),
                    'class_name': contestant.get('class_name', ''),
                    'school': contestant.get('school', ''),
                    'province': contestant.get('province', ''),
                    'city': contestant.get('city', ''),
                    'phone': contestant['phone'],
                    'scores': scores,
                    'final_score': final_score
                })
        
        # 按最终得分降序排列
        rankings.sort(key=lambda x: x['final_score'], reverse=True)
        return rankings
    
    def export_contestants_to_excel(self) -> bytes:
        """导出选手信息到Excel"""
        contestants = self.load_contestants()
        if not contestants:
            return None
        
        df = pd.DataFrame(contestants)
        # 重新排列列的顺序
        columns_order = ['id', 'name', 'gender', 'age', 'class_name', 'school', 'province', 'city', 'phone']
        df = df.reindex(columns=[col for col in columns_order if col in df.columns])
        
        # 重命名列名为中文
        column_names = {
            'id': 'ID',
            'name': '姓名',
            'gender': '性别',
            'age': '年龄',
            'class_name': '班级',
            'school': '学校',
            'province': '省份',
            'city': '城市',
            'phone': '联系电话'
        }
        df = df.rename(columns=column_names)
        
        # 使用BytesIO来创建Excel文件
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='选手信息')
        return output.getvalue()
    
    def export_scores_to_excel(self) -> bytes:
        """导出评分信息到Excel"""
        contestants = self.load_contestants()
        scores_data = self.load_scores()
        
        if not contestants or not scores_data:
            return None
        
        scores_list = []
        for contestant in contestants:
            contestant_id = str(contestant['id'])
            if contestant_id in scores_data:
                scores = scores_data[contestant_id]
                score_row = {
                    'ID': contestant['id'],
                    '姓名': contestant['name'],
                    '性别': contestant.get('gender', ''),
                    '班级': contestant.get('class_name', ''),
                    '学校': contestant.get('school', ''),
                }
                
                # 添加10位评委的分数
                for i, score in enumerate(scores):
                    score_row[f'评委{i+1}'] = score
                
                # 添加统计信息
                score_row['最高分'] = max(scores)
                score_row['最低分'] = min(scores)
                score_row['平均分'] = round(sum(scores) / len(scores), 2)
                score_row['最终得分'] = round(self.calculate_final_score(scores), 2)
                
                scores_list.append(score_row)
        
        df = pd.DataFrame(scores_list)
        
        # 使用BytesIO来创建Excel文件
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='评分详情')
        return output.getvalue()
    
    def export_rankings_to_excel(self) -> bytes:
        """导出排名信息到Excel"""
        rankings = self.get_rankings()
        
        if not rankings:
            return None
        
        ranking_data = []
        for i, contestant in enumerate(rankings):
            if contestant['scores']:
                ranking_data.append({
                    '排名': i + 1,
                    'ID': contestant['id'],
                    '姓名': contestant['name'],
                    '性别': contestant['gender'],
                    '年龄': contestant['age'],
                    '班级': contestant['class_name'],
                    '学校': contestant['school'],
                    '省份': contestant['province'],
                    '城市': contestant['city'],
                    '联系电话': contestant['phone'],
                    '最终得分': round(contestant['final_score'], 2),
                    '最高分': max(contestant['scores']),
                    '最低分': min(contestant['scores']),
                    '平均分': round(sum(contestant['scores']) / len(contestant['scores']), 2)
                })
        
        df = pd.DataFrame(ranking_data)
        
        # 使用BytesIO来创建Excel文件
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='选手排名')
        return output.getvalue()
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        contestants = self.load_contestants()
        scores_data = self.load_scores()
        rankings = self.get_rankings()
        
        stats = {
            'total_contestants': len(contestants),
            'scored_contestants': len([c for c in contestants if str(c['id']) in scores_data]),
            'unscored_contestants': len([c for c in contestants if str(c['id']) not in scores_data]),
            'average_score': 0,
            'highest_score': 0,
            'lowest_score': 0,
            'gender_distribution': {},
            'province_distribution': {},
            'class_distribution': {}
        }
        
        if rankings:
            final_scores = [r['final_score'] for r in rankings if r['final_score'] > 0]
            if final_scores:
                stats['average_score'] = sum(final_scores) / len(final_scores)
                stats['highest_score'] = max(final_scores)
                stats['lowest_score'] = min(final_scores)
        
        # 统计性别分布
        for contestant in contestants:
            gender = contestant.get('gender', '未知')
            stats['gender_distribution'][gender] = stats['gender_distribution'].get(gender, 0) + 1
        
        # 统计省份分布
        for contestant in contestants:
            province = contestant.get('province', '未知')
            stats['province_distribution'][province] = stats['province_distribution'].get(province, 0) + 1
        
        # 统计班级分布
        for contestant in contestants:
            class_name = contestant.get('class_name', '未知')
            stats['class_distribution'][class_name] = stats['class_distribution'].get(class_name, 0) + 1
        
        return stats
