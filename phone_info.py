import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, backref

from base import Base


class QA(Base):
    __tablename__ = "support_qa"
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    qa_type = relationship("User", backref=backref("phones_info", cascade="all, delete-orphan"))
    title = Column(Integer, ForeignKey("bank_branches.id"))
    content = relationship("BankBranch", backref=backref("phones_info", cascade="all, delete-orphan"))
    category = Column(String)
    ref = Column(Integer, default=0)

    def __init__(self, user, bank_branch, phone_number, version, dt=datetime.datetime.now()):
        self.user = user
        self.bank_branch = bank_branch
        self.phone_number = phone_number
        self.version = version
        self.date_time = dt


    qa_type = models.IntegerField(default=0, null=True, verbose_name="نوع سئوال ", choices=Qa_Type)
    title = models.CharField(max_length=100, verbose_name="عنوان")
    content = models.CharField(null=True, max_length=30, verbose_name="محتوا")
    category = models.CharField(null=True, max_length=30, verbose_name="گروه سئوال")
    ref = models.IntegerField(default=0, null=True, verbose_name="ارجاع")

    def __str__(self):
        return str(self.title)  # self.phone_number+','+str(

    class Meta:
        managed: True
        verbose_name = 'سئوال'
        verbose_name_plural = 'سئوال و جواب'
