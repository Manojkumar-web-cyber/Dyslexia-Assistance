import random
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class MentorPersona:
    def __init__(self):
        """
        Initialize AI Mentor Persona
        Meets guideline: "AI persona that delivers warm, personalized, motivational feedback"
        Provides: personalized encouragement, insights, recommendations, session summaries
        """
        self.personality_types = {
            'friendly': self._friendly_feedback,
            'teacher': self._teacher_feedback,
            'calm': self._calm_feedback
        }
        print("MentorPersona initialized - AI Coach Ready")
        
    def generate_feedback(self,
                         reading_history: List[Dict],
                         performance_data: Dict,
                         engagement_data: List[Dict],
                         error_patterns: Dict,
                         learner_age: str = 'teen',
                         personality_preference: str = 'friendly') -> Dict:
        """
        Generate personalized, emotionally intelligent feedback
        """
        
        if not reading_history:
            return self._get_initial_session_feedback(learner_age, personality_preference)
        
        # Analyze performance trends
        trends = self._analyze_trends(reading_history, engagement_data)
        
        # Generate personalized encouragement
        encouragement = self.personality_types.get(
            personality_preference,
            self._friendly_feedback
        )(trends, learner_age)
        
        # Generate insights
        insights = self._generate_insights(trends, reading_history)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(trends, error_patterns, learner_age)
        
        # Generate session summary
        session_summary = self._generate_session_summary(reading_history, engagement_data)
        
        # Generate next steps
        next_steps = self._generate_next_steps(trends, learner_age)
        
        print(f"Mentor feedback generated ({personality_preference} personality)")
        
        return {
            'encouragement': encouragement,
            'insights': insights,
            'recommendations': recommendations,
            'session_summary': session_summary,
            'next_steps': next_steps
        }
    
    def generate_session_summary(self,
                                reading_history: List[Dict],
                                engagement_data: List[Dict]) -> Dict:
        """Generate comprehensive session summary"""
        
        if not reading_history or not engagement_data:
            return {'status': 'No reading data available'}
        
        # Calculate averages
        avg_accuracy = sum(r.get('accuracy_score', 0) for r in reading_history) / len(reading_history)
        avg_engagement = sum(e.get('engagement_score', 0) for e in engagement_data) / len(engagement_data)
        
        improvements = self._identify_improvements(reading_history)
        
        summary = f"""
     Your Session Summary

     Reading Accuracy: {avg_accuracy:.1f}%
     Engagement Level: {avg_engagement:.1f}%
     Passages Completed: {len(reading_history)}
     Session Records: {len(engagement_data)}

     Key Improvements:
{improvements}

  Keep up the great work!
        """
        
        return {
            'summary': summary,
            'metrics': {
                'accuracy': round(avg_accuracy, 2),
                'engagement': round(avg_engagement, 2),
                'passages_completed': len(reading_history),
                'session_records': len(engagement_data)
            }
        }
    
    def _analyze_trends(self, reading_history: List[Dict], engagement_data: List[Dict]) -> Dict:
        """Analyze performance trends"""
        
        if len(reading_history) < 2:
            return {'trend': 'insufficient_data'}
        
        accuracy_scores = [r.get('accuracy_score', 0) for r in reading_history]
        engagement_scores = [e.get('engagement_score', 0) for e in engagement_data]
        
        accuracy_trend = 'improving' if accuracy_scores[-1] > accuracy_scores[0] else 'needs_work'
        engagement_trend = 'improving' if engagement_scores[-1] > engagement_scores[0] else 'declining'
        
        return {
            'accuracy_trend': accuracy_trend,
            'engagement_trend': engagement_trend,
            'avg_accuracy': sum(accuracy_scores) / len(accuracy_scores),
            'avg_engagement': sum(engagement_scores) / len(engagement_scores),
            'highest_accuracy': max(accuracy_scores),
            'lowest_accuracy': min(accuracy_scores)
        }
    
    def _friendly_feedback(self, trends: Dict, learner_age: str) -> str:
        """Generate friendly, encouraging feedback"""
        
        if learner_age == 'child':
            templates = [
                f" Wow! You nailed it today! Your accuracy is at {trends['avg_accuracy']:.1f}%! Keep going!",
                f" You're a superstar! Every time you practice, you get better!",
                f" Amazing effort! You're becoming an awesome reader!"
            ]
        else:
            templates = [
                f"Great work! Your reading accuracy is at {trends['avg_accuracy']:.1f}%. You're making progress!",
                f"Well done! You're showing solid improvement. Keep practicing!",
                f"Nice job! Your engagement is improving. You're on the right track."
            ]
        
        return random.choice(templates)
    
    def _teacher_feedback(self, trends: Dict, learner_age: str) -> str:
        """Generate teacher-like, instructional feedback"""
        
        templates = [
            f"Your accuracy is {trends['avg_accuracy']:.1f}%. Focus on challenging areas to improve further.",
            f"Engagement: {trends['avg_engagement']:.1f}%. Maintain focus and practice regularly.",
            f"Trend: {trends['accuracy_trend']}. Continue consistent practice for better results."
        ]
        
        return random.choice(templates)
    
    def _calm_feedback(self, trends: Dict, learner_age: str) -> str:
        """Generate calm, supportive feedback"""
        
        templates = [
            f"You're at {trends['avg_accuracy']:.1f}% accuracy. That's solid progress!",
            f"Your engagement shows you're focused. Great job staying concentrated!",
            f"You're doing well. Every session builds your reading skills."
        ]
        
        return random.choice(templates)
    
    def _generate_insights(self, trends: Dict, reading_history: List[Dict]) -> List[str]:
        """Generate actionable insights"""
        
        insights = []
        
        if trends['accuracy_trend'] == 'improving':
            improvement = trends['highest_accuracy'] - trends['lowest_accuracy']
            insights.append(f" You improved your pronunciation by {improvement:.1f}%!")
        
        if trends['engagement_trend'] == 'improving':
            insights.append(" Your focus is getting stronger—excellent concentration!")
        
        if reading_history:
            avg_fluency = sum(r.get('fluency_score', 0) for r in reading_history) / len(reading_history)
            insights.append(f" Your reading fluency: {avg_fluency:.1f}/100")
        
        return insights if insights else ["Keep practicing consistently!"]
    
    def _generate_recommendations(self, trends: Dict, error_patterns: Dict, learner_age: str) -> List[str]:
        """Generate personalized recommendations"""
        
        recommendations = []
        
        if trends['avg_accuracy'] < 70:
            recommendations.append("✓ Practice short passages with clearer pronunciation")
        
        if trends['avg_engagement'] < 60:
            recommendations.append("✓ Try reading about topics that interest you")
        
        if trends['accuracy_trend'] == 'needs_work':
            recommendations.append("✓ Focus on common phonetic patterns (th, ch, sh)")
        
        if learner_age == 'child':
            recommendations.append("✓ Read for 10-15 minutes daily for faster improvement!")
        
        return recommendations if recommendations else ["✓ Keep up with regular practice!"]
    
    def _generate_next_steps(self, trends: Dict, learner_age: str) -> List[str]:
        """Generate next steps for continued learning"""
        
        next_steps = [
            "Review words you found challenging",
            "Practice pronunciation of difficult sounds",
            "Read for 15 minutes tomorrow"
        ]
        
        if trends['avg_accuracy'] > 85:
            next_steps.append("Try a more advanced reading level!")
        
        return next_steps
    
    def _identify_improvements(self, reading_history: List[Dict]) -> str:
        """Identify specific improvements"""
        
        if len(reading_history) < 1:
            return "• You've started your reading journey!"
        
        first_accuracy = reading_history[0].get('accuracy_score', 0)
        last_accuracy = reading_history[-1].get('accuracy_score', 0)
        improvement = last_accuracy - first_accuracy
        
        if improvement > 0:
            return f"• Pronunciation improved by {improvement:.1f}%\n• Maintained excellent focus"
        else:
            return "• Tackled challenging words\n• Building reading confidence"
    
    def _get_initial_session_feedback(self, learner_age: str, personality: str) -> Dict:
        """Get feedback for initial session"""
        return {
            'encouragement': "Welcome! Let's start your reading journey! ",
            'insights': ["You're just getting started!"],
            'recommendations': ["Take your time and have fun reading!"],
            'session_summary': "Session started. Keep reading!",
            'next_steps': ["Continue reading the passage"]
        }
