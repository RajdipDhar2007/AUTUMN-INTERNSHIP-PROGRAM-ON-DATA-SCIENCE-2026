# ================================================================================
# Module / Script  : Virtual Makeup Demonstration
# Author           : Dr. Sujoy Kumar Biswas, Ph.D. (EE/CS), M.Tech. (CS)
#                    Head, Research & Innovation
#                    IDEAS - Technology Innovation Hub
#                    Indian Statistical Institute (ISI), Kolkata
# Secondary Affiliation: Founder, AIMP LABS (www.aimplabs.org)
# Target Audience  : IDEAS-TIH Research & Engineering Interns (Autumn 2026)
# --------------------------------------------------------------------------------


import cv2, os, warnings
import numpy as np
import mediapipe as mp


# 1. Suppress verbose C++ and TensorFlow Lite backend logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['GLOG_minloglevel'] = '2'

# 2. Suppress the Python Protobuf UserWarning
warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf")

# -------------------------------------------------------------------------
# 1. Landmark Index Constants
# -------------------------------------------------------------------------
OUTER_LIPS = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291, 375, 321, 405, 314, 17, 84, 181, 91, 146]
INNER_LIPS = [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95]

PALETTE = {
    "Ruby Red":    [50, 20, 200],   # BGR
    "Crimson":     [60, 40, 160],
    "Plum":        [110, 40, 130],
    "Coral":       [90, 100, 230],
    "Natural Tint":[70, 70, 180]
}

def apply_lipstick(frame: np.ndarray, landmarks, bgr_color: list, intensity: float = 0.5) -> np.ndarray:
    """
    Renders realistic virtual lipstick onto the frame.
    
    Args:
        frame: BGR image (H, W, 3)
        landmarks: MediaPipe NormalizedLandmarkList
        bgr_color: Desired lip color [B, G, R]
        intensity: Blending strength in [0.0, 1.0]
    """
    h, w, _ = frame.shape

    # 1. Extract pixel coordinates
    outer_pts = np.array(
        [[int(landmarks.landmark[idx].x * w), int(landmarks.landmark[idx].y * h)] for idx in OUTER_LIPS], 
        dtype=np.int32
    )
    inner_pts = np.array(
        [[int(landmarks.landmark[idx].x * w), int(landmarks.landmark[idx].y * h)] for idx in INNER_LIPS], 
        dtype=np.int32
    )

    # 2. Build 1-bit Lip Mask (Outer polygon minus inner mouth opening)
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.fillPoly(mask, [outer_pts], 255)
    cv2.fillPoly(mask, [inner_pts], 0)

    # 3. Feather the boundary edges (Anti-aliasing)
    # Kernel size (7, 7) creates smooth natural transitions
    mask_feathered = cv2.GaussianBlur(mask, (7, 7), sigmaX=3.0)

    # 4. Synthesize Color Tint (Preserving underlying lip creases)
    color_canvas = np.full_like(frame, bgr_color, dtype=np.uint8)
    
    # Pre-blend color with the original frame so texture & highlights shine through
    tinted_frame = cv2.addWeighted(frame, 1.0 - intensity, color_canvas, intensity, 0)

    # 5. Alpha-composite using feathered mask
    alpha = (mask_feathered.astype(np.float32) / 255.0)[:, :, np.newaxis]
    output = (alpha * tinted_frame + (1.0 - alpha) * frame).astype(np.uint8)

    return output

# -------------------------------------------------------------------------
# 2. Real-Time Processing Loop
# -------------------------------------------------------------------------
def main():
    cap = cv2.VideoCapture(0)
    
    # Initialize MediaPipe Face Mesh
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    color_names = list(PALETTE.keys())
    color_idx = 0

    print("--- Controls ---")
    print(" [C] : Cycle lipstick colors")
    print(" [Q] : Quit")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip horizontally for natural mirror feel
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = face_mesh.process(rgb_frame)

        active_color_name = color_names[color_idx]
        active_bgr = PALETTE[active_color_name]

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                frame = apply_lipstick(frame, face_landmarks, active_bgr, intensity=0.55)

        # UI Overlay
        cv2.putText(
            frame, f"Color: {active_color_name} (Press 'C' to switch)", 
            (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA
        )

        cv2.imshow("Real-Time Virtual Makeup", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            color_idx = (color_idx + 1) % len(color_names)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
