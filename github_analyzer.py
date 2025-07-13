#!/usr/bin/env python3
"""
GitHub Profile Analyzer and Trophy Booster
A tool to analyze GitHub profiles and suggest improvements for earning more trophies.
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class GitHubAnalyzer:
    def __init__(self, username: str, token: Optional[str] = None):
        """
        Initialize the GitHub analyzer
        
        Args:
            username: GitHub username to analyze
            token: GitHub personal access token for API access
        """
        self.username = username
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Trophy-Booster/1.0"
        }
        
        if token:
            self.headers["Authorization"] = f"token {token}"
    
    def get_user_info(self) -> Dict:
        """Get basic user information"""
        try:
            response = requests.get(f"{self.base_url}/users/{self.username}", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching user info: {e}")
            return {}
    
    def get_repositories(self) -> List[Dict]:
        """Get all public repositories"""
        try:
            repos = []
            page = 1
            while True:
                response = requests.get(
                    f"{self.base_url}/users/{self.username}/repos",
                    params={"page": page, "per_page": 100, "sort": "updated"},
                    headers=self.headers
                )
                response.raise_for_status()
                page_repos = response.json()
                
                if not page_repos:
                    break
                    
                repos.extend(page_repos)
                page += 1
            
            return repos
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repositories: {e}")
            return []
    
    def analyze_profile(self) -> Dict:
        """Analyze the GitHub profile and provide insights"""
        user_info = self.get_user_info()
        repositories = self.get_repositories()
        
        if not user_info:
            return {"error": "Unable to fetch user information"}
        
        # Calculate metrics
        total_stars = sum(repo['stargazers_count'] for repo in repositories)
        total_forks = sum(repo['forks_count'] for repo in repositories)
        languages = {}
        
        for repo in repositories:
            if repo['language']:
                languages[repo['language']] = languages.get(repo['language'], 0) + 1
        
        # Recent activity (last 30 days)
        recent_repos = [
            repo for repo in repositories
            if self._is_recent_activity(repo['updated_at'])
        ]
        
        analysis = {
            "profile_summary": {
                "username": user_info.get('login'),
                "name": user_info.get('name'),
                "bio": user_info.get('bio'),
                "location": user_info.get('location'),
                "company": user_info.get('company'),
                "blog": user_info.get('blog'),
                "followers": user_info.get('followers', 0),
                "following": user_info.get('following', 0),
                "public_repos": user_info.get('public_repos', 0),
                "created_at": user_info.get('created_at')
            },
            "repository_metrics": {
                "total_repositories": len(repositories),
                "total_stars": total_stars,
                "total_forks": total_forks,
                "average_stars_per_repo": total_stars / len(repositories) if repositories else 0,
                "top_languages": dict(sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]),
                "recent_activity": len(recent_repos)
            },
            "trophy_potential": self._calculate_trophy_potential(user_info, repositories),
            "recommendations": self._generate_recommendations(user_info, repositories)
        }
        
        return analysis
    
    def _is_recent_activity(self, updated_at: str) -> bool:
        """Check if the activity is within the last 30 days"""
        try:
            updated_date = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
            thirty_days_ago = datetime.now(updated_date.tzinfo) - timedelta(days=30)
            return updated_date > thirty_days_ago
        except ValueError:
            return False
    
    def _calculate_trophy_potential(self, user_info: Dict, repositories: List[Dict]) -> Dict:
        """Calculate potential for earning different trophies"""
        total_stars = sum(repo['stargazers_count'] for repo in repositories)
        followers = user_info.get('followers', 0)
        public_repos = user_info.get('public_repos', 0)
        
        # Trophy thresholds (approximate)
        trophy_levels = {
            "commits": {"bronze": 100, "silver": 500, "gold": 1000},
            "repositories": {"bronze": 10, "silver": 50, "gold": 100},
            "stars": {"bronze": 50, "silver": 200, "gold": 500},
            "followers": {"bronze": 10, "silver": 50, "gold": 100},
            "issues": {"bronze": 10, "silver": 50, "gold": 100},
            "pull_requests": {"bronze": 10, "silver": 50, "gold": 100}
        }
        
        potential = {
            "stars": {
                "current": total_stars,
                "next_level": self._get_next_level(total_stars, trophy_levels["stars"]),
                "potential": "high" if total_stars < 50 else "medium"
            },
            "followers": {
                "current": followers,
                "next_level": self._get_next_level(followers, trophy_levels["followers"]),
                "potential": "high" if followers < 10 else "medium"
            },
            "repositories": {
                "current": public_repos,
                "next_level": self._get_next_level(public_repos, trophy_levels["repositories"]),
                "potential": "medium" if public_repos < 50 else "low"
            }
        }
        
        return potential
    
    def _get_next_level(self, current: int, levels: Dict) -> str:
        """Get the next trophy level based on current value"""
        if current < levels["bronze"]:
            return f"bronze ({levels['bronze'] - current} more needed)"
        elif current < levels["silver"]:
            return f"silver ({levels['silver'] - current} more needed)"
        elif current < levels["gold"]:
            return f"gold ({levels['gold'] - current} more needed)"
        else:
            return "gold achieved!"
    
    def _generate_recommendations(self, user_info: Dict, repositories: List[Dict]) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Profile completeness
        if not user_info.get('bio'):
            recommendations.append("Add a compelling bio to your profile")
        
        if not user_info.get('location'):
            recommendations.append("Add your location to help others connect")
        
        if not user_info.get('blog'):
            recommendations.append("Add a blog or portfolio link to showcase your work")
        
        # Repository analysis
        total_stars = sum(repo['stargazers_count'] for repo in repositories)
        if total_stars < 10:
            recommendations.append("Focus on creating useful projects that can attract stars")
        
        # Documentation
        repos_without_description = [repo for repo in repositories if not repo.get('description')]
        if len(repos_without_description) > 3:
            recommendations.append("Add descriptions to your repositories")
        
        # Activity
        if user_info.get('followers', 0) < 5:
            recommendations.append("Engage with the community to gain followers")
        
        # Language diversity
        languages = set(repo['language'] for repo in repositories if repo['language'])
        if len(languages) < 3:
            recommendations.append("Explore different programming languages to showcase versatility")
        
        return recommendations

def main():
    """Main function to run the analyzer"""
    print("🏆 GitHub Profile Analyzer & Trophy Booster")
    print("=" * 50)
    
    username = input("Enter GitHub username to analyze: ").strip()
    
    if not username:
        print("❌ Please provide a valid username")
        return
    
    analyzer = GitHubAnalyzer(username)
    analysis = analyzer.analyze_profile()
    
    if "error" in analysis:
        print(f"❌ {analysis['error']}")
        return
    
    # Display results
    profile = analysis["profile_summary"]
    metrics = analysis["repository_metrics"]
    potential = analysis["trophy_potential"]
    recommendations = analysis["recommendations"]
    
    print(f"\n👤 Profile: {profile['name']} (@{profile['username']})")
    print(f"📊 Repositories: {profile['public_repos']}")
    print(f"⭐ Total Stars: {metrics['total_stars']}")
    print(f"👥 Followers: {profile['followers']}")
    print(f"📈 Following: {profile['following']}")
    
    print(f"\n🏆 Trophy Potential:")
    for trophy, data in potential.items():
        print(f"  {trophy.title()}: {data['current']} → {data['next_level']}")
    
    print(f"\n💡 Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec}")
    
    print(f"\n🔝 Top Languages:")
    for lang, count in metrics['top_languages'].items():
        print(f"  {lang}: {count} repositories")

if __name__ == "__main__":
    main()
