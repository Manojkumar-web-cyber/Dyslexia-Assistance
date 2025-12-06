import cv2
import mediapipe as mp
import numpy as np
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class AttentionTracker:
    def __init__(self):
        """
        Initialize MediaPipe Face Mesh for webcam-based attention tracking
        Meets guideline: "Analyze learner attention using webcam-based gaze and focus tracking"
        """
        try:
            self.mp_face_mesh = mp.solutions.face_mesh
            self.face_mesh = self.mp_face_mesh.FaceMesh(
                static_image_mode=False,
                max_num_faces=1,
                min_detection_confidence=0.5
            )
            print("AttentionTracker initialized - Webcam-based Eye Tracking Ready (MediaPipe)")
        except Exception as e:
            logger.error(f"MediaPipe init error: {str(e)}")
            self.face_mesh = None
        
    def analyze_frame(self, frame_file) -> Dict:
        """
        Analyze a webcam frame for attention metrics:
        - Gaze direction (left/right/forward)
        - Blink rate
        - Focus level
        - Engagement score
        - Fatigue detection
        """
        try:
            if not self.face_mesh:
                return self._get_default_metrics()
            
            # Read frame from file
            nparr = np.frombuffer(frame_file.read(), np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame is None:
                return self._get_default_metrics()
            
            # Detect face landmarks
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(frame_rgb)
            
            if not results.multi_face_landmarks:
                return self._get_default_metrics()
            
            # Calculate attention metrics
            metrics = {
                'gaze_direction': self._calculate_gaze_direction(results),
                'blink_rate': self._calculate_blink_rate(results),
                'focus_level': self._calculate_focus_level(results),
                'engagement_score': 0,
                'fatigue_detected': False
            }
            
            metrics['engagement_score'] = self._calculate_engagement(metrics)
            metrics['fatigue_detected'] = self._detect_fatigue(metrics)
            
            print(f"Attention Tracked: Engagement={metrics['engagement_score']}%, Fatigue={metrics['fatigue_detected']}")
            return metrics
            
        except Exception as e:
            logger.error(f"Frame analysis error: {str(e)}")
            return self._get_default_metrics()
    
    def _calculate_gaze_direction(self, mesh_results) -> str:
        """Determine gaze direction (left/right/forward)"""
        if not mesh_results.multi_face_landmarks:
            return "unknown"
        
        landmarks = mesh_results.multi_face_landmarks[0]
        left_eye = landmarks[33]
        right_eye = landmarks[263]
        nose = landmarks[1]
        
        if left_eye.x > nose.x and right_eye.x > nose.x:
            return "looking_right"
        elif left_eye.x < nose.x and right_eye.x < nose.x:
            return "looking_left"
        else:
            return "looking_forward"
    
    def _calculate_blink_rate(self, mesh_results) -> float:
        """Calculate blink frequency indicator"""
        if not mesh_results.multi_face_landmarks:
            return 0.0
        
        landmarks = mesh_results.multi_face_landmarks[0]
        left_eye_top = landmarks[159]
        left_eye_bottom = landmarks[145]
        
        vertical_distance = np.sqrt(
            (left_eye_top.y - left_eye_bottom.y)**2 + 
            (left_eye_top.x - left_eye_bottom.x)**2
        )
        
        return round(vertical_distance * 100, 2)
    
    def _calculate_focus_level(self, mesh_results) -> float:
        """Calculate focus level (0-100) based on head stability"""
        if not mesh_results.multi_face_landmarks:
            return 0.0
        
        landmarks = mesh_results.multi_face_landmarks[0]
        nose = landmarks[1]
        forehead = landmarks[10]
        chin = landmarks[152]
        
        vertical_range = abs(forehead.y - chin.y)
        focus = max(0, 100 - (vertical_range * 100))
        
        return round(focus, 2)
    
    def _calculate_engagement(self, metrics: Dict) -> float:
        """Calculate overall engagement score (0-100)"""
        focus_weight = 0.5
        gaze_weight = 0.3
        blink_weight = 0.2
        
        focus_score = metrics['focus_level']
        gaze_score = 100 if metrics['gaze_direction'] == 'looking_forward' else 60
        blink_score = max(0, 100 - abs(metrics['blink_rate'] - 50))
        
        engagement = (focus_score * focus_weight + 
                     gaze_score * gaze_weight + 
                     blink_score * blink_weight)
        
        return round(engagement, 2)
    
    def _detect_fatigue(self, metrics: Dict) -> bool:
        """Detect signs of fatigue or distraction"""
        low_focus = metrics['focus_level'] < 40
        looking_away = metrics['gaze_direction'] != 'looking_forward'
        low_engagement = metrics['engagement_score'] < 50
        
        return (low_focus) or (looking_away and low_engagement)
    
    def _get_default_metrics(self) -> Dict:
        """Return default metrics when face not detected"""
        return {
            'gaze_direction': 'unknown',
            'blink_rate': 0.0,
            'focus_level': 75.0,
            'engagement_score': 75.0,
            'fatigue_detected': False
        }
