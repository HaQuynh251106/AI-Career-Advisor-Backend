import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import google.generativeai as genai
from app.models.job_listings import JobListing
from app.core.config import settings

# Cấu hình API Key từ biến môi trường (An toàn hơn hardcode)
if settings.GEMINI_API_KEY:
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
    except Exception as e:
        print(f"❌ Lỗi cấu hình Key: {e}")
        exit(1)
else:
    print("❌ Lỗi: Chưa tìm thấy GEMINI_API_KEY trong file .env")
    exit(1)

async def main():
    # 1. Kết nối DB
    print("🔌 Đang kết nối Database...")
    try:
        client = AsyncIOMotorClient(settings.MONGO_URI)
        # Khởi tạo Beanie chỉ với model JobListing là đủ cho script này
        await init_beanie(database=client.get_database(), document_models=[JobListing])
    except Exception as e:
        print(f"❌ Lỗi kết nối DB: {e}")
        return

    print("🔄 Đang lấy danh sách việc làm từ Database...")
    jobs = await JobListing.find_all().to_list()
    
    if not jobs:
        print("⚠️ Database đang trống. Bạn hãy chạy 'python seed_jobs_30.py' trước nhé!")
        return

    print(f"🚀 Tìm thấy {len(jobs)} công việc. Bắt đầu tạo Vector...")

    count = 0
    for job in jobs:
        count += 1
        # Tạo nội dung để biến thành vector (gộp tiêu đề + mô tả + kỹ năng)
        # Việc gộp này giúp AI hiểu ngữ cảnh tốt hơn
        text_to_embed = f"{job.title}. {job.description}. Kỹ năng: {', '.join(job.skills_required)}"
        
        print(f"⚡ [{count}/{len(jobs)}] Đang xử lý: {job.title}...")
        
        # Gọi Gemini tạo vector
        try:
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=text_to_embed
            )
            job.vector = result['embedding']
            await job.save() # Lưu ngược lại vào DB
        except Exception as e:
            print(f"❌ Lỗi khi gọi Gemini: {e}")

    print("\n✅ HOÀN TẤT! Đã cập nhật Vector cho toàn bộ công việc.")

if __name__ == "__main__":
    asyncio.run(main())
