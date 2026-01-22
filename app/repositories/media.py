from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Attachment


class MediaRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upload_file(self, file_path: str):
        new_file = Attachment(path=file_path)
        self.session.add(new_file)
        await self.session.commit()
        await self.session.refresh(new_file)

        return new_file
