from datetime import datetime, timedelta, timezone

class TimeHandler:

    def utc_now(self) -> datetime:
        return datetime.now(timezone.utc)
    
    def expiry_at(self, seconds: int) -> datetime:
        return datetime.now(timezone.utc) + timedelta(seconds=seconds)
    
    def datetime_to_unix_timestamp(self, date: datetime) -> str:
        return str(date.timestamp())
    
    def datetime_from_unix_timestamp(self, timestamp: str) -> datetime:
        return datetime.fromtimestamp(float(timestamp), timezone.utc)
    
    def datetime_from_str(self, date_string: str) -> datetime:
        """Format: '%Y-%m-%d %H:%M:%S'"""
        return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    

    def is_expired(self, timestamp: str) -> bool:
    
        expiry_time = int(float(timestamp))

        if int(float(self.datetime_to_unix_timestamp(self.utc_now()))) < expiry_time:
            return False

        return True