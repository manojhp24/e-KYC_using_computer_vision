from services.face.face_service import FaceService


def main() -> None:

    face_service = FaceService()

    is_match = face_service.verify_faces(
        "uploads/ids/55617593-160f-4ab1-a287-43a468faa0fd.jpeg",
        "uploads/live/image copy.png",
    )

    print(f"Match: {is_match}")


if __name__ == "__main__":
    main()