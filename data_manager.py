import json
import os
from typing import Dict, List, Any

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
                    'phone': contestant['phone'],
                    'scores': scores,
                    'final_score': final_score
                })
        
        # 按最终得分降序排列
        rankings.sort(key=lambda x: x['final_score'], reverse=True)
        return rankings 