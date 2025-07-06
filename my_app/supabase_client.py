import os
import json
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

from my_app.core import TranslationJob


class SupabaseClient:
    """Supabase client for file storage and logging"""
    
    def __init__(self):
        self.supabase: Optional[Client] = None
        self.storage_bucket = "translation-files"
        self.logs_bucket = "translation-logs"
        
        if SUPABASE_AVAILABLE:
            self.supabase_url = os.getenv("SUPABASE_URL")
            self.supabase_service_key = os.getenv("SUPABASE_SERVICE_KEY")
            
            if self.supabase_url and self.supabase_service_key:
                self.supabase = create_client(self.supabase_url, self.supabase_service_key)
    
    def is_available(self) -> bool:
        """Check if Supabase is available and configured"""
        return SUPABASE_AVAILABLE and self.supabase is not None
    
    def upload_file(self, local_path: str, supabase_path: str, bucket: str = None) -> Dict[str, Any]:
        """Upload file to Supabase Storage"""
        if not self.is_available():
            return {"error": "Supabase not available"}
        
        bucket = bucket or self.storage_bucket
        
        try:
            with open(local_path, "rb") as file_data:
                res = self.supabase.storage.from_(bucket).upload(supabase_path, file_data)
            
            if res.get("error"):
                return {"error": f"Upload failed: {res['error']}"}
            
            # Get public URL
            public_url = self.supabase.storage.from_(bucket).get_public_url(supabase_path)
            
            return {
                "success": True,
                "path": supabase_path,
                "public_url": public_url,
                "bucket": bucket
            }
            
        except Exception as e:
            return {"error": f"Upload failed: {str(e)}"}
    
    def upload_translation_output(self, job: TranslationJob) -> Dict[str, Any]:
        """Upload translation output file to Supabase Storage"""
        if not job.output_file or not os.path.exists(job.output_file):
            return {"error": "Output file not found"}
        
        # Generate Supabase path
        filename = os.path.basename(job.output_file)
        supabase_path = f"translations/{job.config.user_id}/{job.config.job_id}/{filename}"
        
        return self.upload_file(job.output_file, supabase_path, self.storage_bucket)
    
    def upload_log_file(self, job: TranslationJob, log_content: str) -> Dict[str, Any]:
        """Upload log content to Supabase Storage"""
        if not self.is_available():
            return {"error": "Supabase not available"}
        
        # Create temporary log file
        log_filename = f"translation_log_{job.config.job_id}.json"
        temp_log_path = f"/tmp/{log_filename}"
        
        try:
            with open(temp_log_path, "w") as f:
                f.write(log_content)
            
            # Upload to Supabase
            supabase_path = f"logs/{job.config.user_id}/{job.config.job_id}/{log_filename}"
            result = self.upload_file(temp_log_path, supabase_path, self.logs_bucket)
            
            # Clean up temp file
            os.unlink(temp_log_path)
            
            return result
            
        except Exception as e:
            return {"error": f"Log upload failed: {str(e)}"}
    
    def log_translation_run(self, job: TranslationJob) -> Dict[str, Any]:
        """Log translation run to Supabase database"""
        if not self.is_available():
            return {"error": "Supabase not available"}
        
        try:
            # Prepare log data
            log_data = {
                "user_id": job.config.user_id,
                "job_id": job.config.job_id,
                "book_path": job.config.book_path,
                "model": job.config.model,
                "language": job.config.language,
                "status": job.status,
                "output_file": job.output_file,
                "error": job.error,
                "token_usage": job.token_usage,
                "created_at": job.created_at.isoformat(),
                "started_at": job.started_at.isoformat() if job.started_at else None,
                "completed_at": job.completed_at.isoformat() if job.completed_at else None,
                "config": {
                    "prompt": job.config.prompt,
                    "batch_size": job.config.batch_size,
                    "single_translate": job.config.single_translate,
                    "temperature": job.config.temperature,
                    "test": job.config.test,
                    "test_num": job.config.test_num,
                    "accumulated_num": job.config.accumulated_num,
                    "block_size": job.config.block_size
                }
            }
            
            # Insert into database
            result = self.supabase.table("translation_runs").insert(log_data).execute()
            
            if result.data:
                return {"success": True, "log_id": result.data[0]["id"]}
            else:
                return {"error": "Failed to insert log"}
            
        except Exception as e:
            return {"error": f"Database logging failed: {str(e)}"}
    
    def get_user_translations(self, user_id: str, limit: int = 50) -> Dict[str, Any]:
        """Get user's translation history from database"""
        if not self.is_available():
            return {"error": "Supabase not available"}
        
        try:
            result = self.supabase.table("translation_runs").select("*").eq("user_id", user_id).limit(limit).order("created_at", desc=True).execute()
            
            return {
                "success": True,
                "translations": result.data,
                "count": len(result.data)
            }
            
        except Exception as e:
            return {"error": f"Failed to fetch translations: {str(e)}"}
    
    def get_translation_by_job_id(self, job_id: str, user_id: str) -> Dict[str, Any]:
        """Get specific translation by job ID"""
        if not self.is_available():
            return {"error": "Supabase not available"}
        
        try:
            result = self.supabase.table("translation_runs").select("*").eq("job_id", job_id).eq("user_id", user_id).execute()
            
            if result.data:
                return {"success": True, "translation": result.data[0]}
            else:
                return {"error": "Translation not found"}
            
        except Exception as e:
            return {"error": f"Failed to fetch translation: {str(e)}"}
    
    def create_signed_url(self, file_path: str, bucket: str = None, expires_in: int = 3600) -> Dict[str, Any]:
        """Create signed URL for file download"""
        if not self.is_available():
            return {"error": "Supabase not available"}
        
        bucket = bucket or self.storage_bucket
        
        try:
            signed_url = self.supabase.storage.from_(bucket).create_signed_url(file_path, expires_in)
            
            return {
                "success": True,
                "signed_url": signed_url,
                "expires_in": expires_in
            }
            
        except Exception as e:
            return {"error": f"Failed to create signed URL: {str(e)}"}
    
    def delete_file(self, file_path: str, bucket: str = None) -> Dict[str, Any]:
        """Delete file from Supabase Storage"""
        if not self.is_available():
            return {"error": "Supabase not available"}
        
        bucket = bucket or self.storage_bucket
        
        try:
            result = self.supabase.storage.from_(bucket).remove([file_path])
            
            return {"success": True, "deleted": result}
            
        except Exception as e:
            return {"error": f"Failed to delete file: {str(e)}"}
    
    def ensure_buckets_exist(self) -> Dict[str, Any]:
        """Ensure required storage buckets exist"""
        if not self.is_available():
            return {"error": "Supabase not available"}
        
        try:
            # Get existing buckets
            buckets = self.supabase.storage.list_buckets()
            existing_bucket_names = [bucket.name for bucket in buckets]
            
            created_buckets = []
            
            # Create translation files bucket if it doesn't exist
            if self.storage_bucket not in existing_bucket_names:
                self.supabase.storage.create_bucket(self.storage_bucket)
                created_buckets.append(self.storage_bucket)
            
            # Create logs bucket if it doesn't exist
            if self.logs_bucket not in existing_bucket_names:
                self.supabase.storage.create_bucket(self.logs_bucket)
                created_buckets.append(self.logs_bucket)
            
            return {
                "success": True,
                "created_buckets": created_buckets,
                "existing_buckets": existing_bucket_names
            }
            
        except Exception as e:
            return {"error": f"Failed to ensure buckets: {str(e)}"}


# Global Supabase client instance
supabase_client = SupabaseClient()


def get_supabase_client() -> SupabaseClient:
    """Get global Supabase client instance"""
    return supabase_client


def process_translation_completion(job: TranslationJob) -> Dict[str, Any]:
    """Process translation completion by uploading files and logging"""
    results = {}
    
    if job.status == "completed" and job.output_file:
        # Upload output file
        upload_result = supabase_client.upload_translation_output(job)
        results["file_upload"] = upload_result
        
        # Create log content
        log_content = json.dumps({
            "job_id": job.config.job_id,
            "user_id": job.config.user_id,
            "status": job.status,
            "config": {
                "book_path": job.config.book_path,
                "model": job.config.model,
                "language": job.config.language,
                "prompt": job.config.prompt,
                "single_translate": job.config.single_translate,
                "temperature": job.config.temperature
            },
            "output_file": job.output_file,
            "token_usage": job.token_usage,
            "created_at": job.created_at.isoformat(),
            "started_at": job.started_at.isoformat() if job.started_at else None,
            "completed_at": job.completed_at.isoformat() if job.completed_at else None,
            "processing_time": (job.completed_at - job.started_at).total_seconds() if job.completed_at and job.started_at else None
        }, indent=2)
        
        # Upload log
        log_result = supabase_client.upload_log_file(job, log_content)
        results["log_upload"] = log_result
    
    # Log to database
    db_result = supabase_client.log_translation_run(job)
    results["db_log"] = db_result
    
    return results