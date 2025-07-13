#!/usr/bin/env python3
"""
Trophy Tracker - Monitor your GitHub trophy progress
"""

import json
import os
from datetime import datetime
from github_analyzer import GitHubAnalyzer

class TrophyTracker:
    def __init__(self, username: str):
        self.username = username
        self.data_file = f"{username}_trophy_data.json"
        self.analyzer = GitHubAnalyzer(username)
    
    def load_history(self):
        """Load historical trophy data"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {"history": []}
    
    def save_snapshot(self, data):
        """Save current trophy snapshot"""
        history = self.load_history()
        
        snapshot = {
            "date": datetime.now().isoformat(),
            "data": data
        }
        
        history["history"].append(snapshot)
        
        with open(self.data_file, 'w') as f:
            json.dump(history, f, indent=2)
    
    def track_progress(self):
        """Track and display trophy progress"""
        print(f"📊 Tracking trophies for @{self.username}")
        print("=" * 50)
        
        current_data = self.analyzer.analyze_profile()
        
        if "error" in current_data:
            print(f"❌ {current_data['error']}")
            return
        
        # Save snapshot
        self.save_snapshot(current_data)
        
        # Display current stats
        profile = current_data["profile_summary"]
        metrics = current_data["repository_metrics"]
        
        print(f"📈 Current Stats:")
        print(f"  ⭐ Stars: {metrics['total_stars']}")
        print(f"  👥 Followers: {profile['followers']}")
        print(f"  📚 Repositories: {profile['public_repos']}")
        print(f"  🍴 Total Forks: {metrics['total_forks']}")
        
        # Show trophy potential
        potential = current_data["trophy_potential"]
        print(f"\n🏆 Trophy Progress:")
        for trophy, data in potential.items():
            print(f"  {trophy.title()}: {data['current']} → {data['next_level']}")
        
        # Show recommendations
        recommendations = current_data["recommendations"]
        if recommendations:
            print(f"\n💡 Action Items:")
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"  {i}. {rec}")
        
        # Show historical progress if available
        history = self.load_history()
        if len(history["history"]) > 1:
            print(f"\n📊 Progress Since Last Check:")
            prev_data = history["history"][-2]["data"]
            self._show_progress_diff(prev_data, current_data)
    
    def _show_progress_diff(self, prev_data, current_data):
        """Show difference between current and previous data"""
        prev_metrics = prev_data["repository_metrics"]
        current_metrics = current_data["repository_metrics"]
        
        star_diff = current_metrics["total_stars"] - prev_metrics["total_stars"]
        follower_diff = current_data["profile_summary"]["followers"] - prev_data["profile_summary"]["followers"]
        repo_diff = current_data["profile_summary"]["public_repos"] - prev_data["profile_summary"]["public_repos"]
        
        if star_diff > 0:
            print(f"  ⭐ +{star_diff} stars")
        if follower_diff > 0:
            print(f"  👥 +{follower_diff} followers")
        if repo_diff > 0:
            print(f"  📚 +{repo_diff} repositories")

def main():
    """Main function"""
    username = input("Enter your GitHub username: ").strip()
    
    if not username:
        print("❌ Please provide a valid username")
        return
    
    tracker = TrophyTracker(username)
    tracker.track_progress()

if __name__ == "__main__":
    main()
