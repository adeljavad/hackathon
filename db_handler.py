import datetime
import os

from sqlalchemy import desc, cast, Date

from balebot.utils.logger import Logger
from bot.models.address_info import AddressInfo
from bot.models.address_info_log import AddressInfoLog
from bot.models.admin import Admin
from bot.models.admin_migrate_table import AdminMigrate
from bot.models.bank_branch import BankBranch
from bot.models.base import Session
from bot.models.description_info import DescriptionInfo
from bot.models.description_info_log import DescriptionInfoLog
from bot.models.like import Like
from bot.models.location_info import LocationInfo
from bot.models.location_info_log import LocationInfoLog
from bot.models.migrate_table import Migrate
from bot.models.phone_info import PhoneInfo
from bot.models.phone_info_log import PhoneInfoLog
from bot.models.user import User
from config import BotConfig
from constants import LogMessage, UserData, InfoTypes

session = Session()
my_logger = Logger.get_logger()


def is_migrated() -> bool:
    migrate = session.query(Migrate).one_or_none()
    if not migrate:
        session.add(Migrate())
        session.commit()
        return False
    else:
        return True


def is_admin_migrated() -> bool:
    migrate = session.query(AdminMigrate).one_or_none()
    if not migrate:
        session.add(AdminMigrate())
        session.commit()
        return False
    else:
        return True


def get_admins():
    admins = session.query(Admin).all()
    return admins


def is_admin(peer_id, access_hash):
    admin = session.query(Admin).filter(Admin.peer_id == peer_id).one_or_none()
    if admin:
        if not admin.access_hash:
            admin.access_hash = access_hash
            session.commit()
    return admin


def add_user(user):
    if get_user(user.id):
        return
    user = User(user.id, user.access_hash, name=user.name, user_name=user.username, sex=user.sex)
    session.add(user)
    session.commit()
    my_logger.info(LogMessage.user_register,
                   extra={UserData.user_id: user.id, "tag": "info"})


def get_user(peer_id) -> User:
    user = session.query(User).filter(User.peer_id == peer_id).one_or_none()
    return user


def get_user_contributed_branch(info_type, user) -> {str}:
    user = get_user(user.peer_id)
    contribution_branch_ids = None
    res = set()
    if info_type == InfoTypes.location:
        contribution_branch_ids = session.query(BankBranch.branch_id).join(LocationInfo).filter(
            LocationInfo.user_id == user.id).all()
    if info_type == InfoTypes.phone:
        contribution_branch_ids = session.query(BankBranch.branch_id).join(PhoneInfo).filter(
            PhoneInfo.user_id == user.id).all()
    if info_type == InfoTypes.address:
        contribution_branch_ids = session.query(BankBranch.branch_id).join(AddressInfo).filter(
            AddressInfo.user_id == user.id).all()
    if info_type == InfoTypes.description:
        contribution_branch_ids = session.query(BankBranch.branch_id).join(DescriptionInfo).filter(
            DescriptionInfo.user_id == user.id).all()

    for branch_id in contribution_branch_ids:
        res.add(branch_id[0])
    return res


def get_branch(branch_id) -> BankBranch:
    return session.query(BankBranch).filter(BankBranch.branch_id == branch_id).one_or_none()


def get_base_location_info(branch_id) -> LocationInfo:
    bank_branch = get_branch(branch_id)
    return session.query(LocationInfo).filter(LocationInfo.bank_branch == bank_branch,
                                              LocationInfo.version == 0).one_or_none()


def add_location_info(branch_id, location, user):
    user = get_user(user.peer_id)
    bank_branch = get_branch(branch_id)
    last_info = get_location_info(branch_id)
    new_version = last_info.version + 1 if last_info else 1
    location_info = LocationInfo(user, bank_branch, location.latitude, location.longitude, new_version)
    session.add(location_info)
    session.commit()


def get_location_info(branch_id) -> LocationInfo:
    bank_branch = get_branch(branch_id)
    return session.query(LocationInfo).filter(LocationInfo.bank_branch == bank_branch).order_by(
        desc(LocationInfo.version)).limit(1).one_or_none()


def get_user_location_info(branch_id, user) -> LocationInfo:
    user = get_user(user.peer_id)
    bank_branch = get_branch(branch_id)
    location_info = session.query(LocationInfo).filter(LocationInfo.bank_branch == bank_branch,
                                                       LocationInfo.user_id == user.id).order_by(
        desc(LocationInfo.version)).limit(1).one_or_none()
    return location_info


def del_location_info(branch_id, user, delete_object=None):
    location_info = delete_object if delete_object else get_location_info(branch_id)
    if not user.peer_id == location_info.user.peer_id:
        return False
    log_location = LocationInfoLog(location_info)
    log_location.id = location_info.id
    session.add(log_location)
    session.delete(location_info)
    session.commit()
    return True


def add_phone_info(branch_id, phone, user):
    user = get_user(user.peer_id)
    bank_branch = get_branch(branch_id)
    last_info = get_phone_info(branch_id)
    new_version = last_info.version + 1 if last_info else 1
    phone_info = PhoneInfo(user, bank_branch, phone, new_version)
    session.add(phone_info)
    session.commit()


def get_phone_info(branch_id) -> PhoneInfo:
    bank_branch = get_branch(branch_id)
    return session.query(PhoneInfo).filter(PhoneInfo.bank_branch == bank_branch).order_by(
        desc(PhoneInfo.version)).limit(1).one_or_none()


def get_user_phone_info(branch_id, user) -> PhoneInfo:
    user = get_user(user.peer_id)
    bank_branch = get_branch(branch_id)
    phone_info = session.query(PhoneInfo).filter(PhoneInfo.bank_branch == bank_branch,
                                                 PhoneInfo.user_id == user.id).order_by(
        desc(PhoneInfo.version)).limit(1).one_or_none()
    return phone_info


def del_phone_info(branch_id, user, delete_object=None):
    phone_info = delete_object if delete_object else get_phone_info(branch_id)
    if not user.peer_id == phone_info.user.peer_id:
        return False
    log_phone = PhoneInfoLog(phone_info)
    log_phone.id = phone_info.id
    session.add(log_phone)
    session.delete(phone_info)
    session.commit()
    return True


def add_address_info(branch_id, address, user):
    user = get_user(user.peer_id)
    bank_branch = get_branch(branch_id)
    last_info = get_address_info(branch_id)
    new_version = last_info.version + 1 if last_info else 1
    address_info = AddressInfo(user, bank_branch, address, new_version)
    session.add(address_info)
    session.commit()


def get_address_info(branch_id) -> AddressInfo:
    bank_branch = get_branch(branch_id)
    return session.query(AddressInfo).filter(AddressInfo.bank_branch == bank_branch).order_by(
        desc(AddressInfo.version)).limit(1).one_or_none()


def get_user_address_info(branch_id, user) -> AddressInfo:
    user = get_user(user.peer_id)
    bank_branch = get_branch(branch_id)
    address_info = session.query(AddressInfo).filter(AddressInfo.bank_branch == bank_branch,
                                                     AddressInfo.user_id == user.id).order_by(
        desc(AddressInfo.version)).limit(1).one_or_none()
    return address_info


def del_address_info(branch_id, user, delete_object=None):
    address_info = delete_object if delete_object else get_address_info(branch_id)
    if not user.peer_id == address_info.user.peer_id:
        return False
    log_address = AddressInfoLog(address_info)
    log_address.id = address_info.id
    session.add(log_address)
    session.delete(address_info)
    session.commit()
    return True


def add_description_info(branch_id, description, user):
    user = get_user(user.peer_id)
    bank_branch = get_branch(branch_id)
    last_info = get_description_info(branch_id)
    new_version = last_info.version + 1 if last_info else 1
    description_info = DescriptionInfo(user, bank_branch, description, new_version)
    session.add(description_info)
    session.commit()


def get_description_info(branch_id) -> DescriptionInfo:
    bank_branch = get_branch(branch_id)
    return session.query(DescriptionInfo).filter(DescriptionInfo.bank_branch == bank_branch).order_by(
        desc(DescriptionInfo.version)).limit(1).one_or_none()


def get_user_description_info(branch_id, user) -> DescriptionInfo:
    user = get_user(user.peer_id)
    bank_branch = get_branch(branch_id)
    description_info = session.query(DescriptionInfo).filter(DescriptionInfo.bank_branch == bank_branch,
                                                             DescriptionInfo.user_id == user.id).order_by(
        desc(DescriptionInfo.version)).limit(1).one_or_none()
    return description_info


def del_description_info(branch_id, user, delete_object=None):
    description_info = delete_object if delete_object else get_user_description_info(branch_id, user)
    if not user.peer_id == description_info.user.peer_id:
        return False
    log_description = DescriptionInfoLog(description_info)
    log_description.id = description_info.id
    session.add(log_description)
    session.delete(description_info)
    session.commit()
    return True


def delete_branch_info(delete_object):
    session.delete(delete_object)
    session.commit()


# def get_confirmed_info(info_type, bank_branch_id, user_id):
#     if InfoTypes.location == info_type:
#         return session.query(LocationInfoLog).filter(LocationInfoLog.user_id == user_id,
#                                                      LocationInfoLog.bank_branch_id == bank_branch_id)
#     if InfoTypes.phone == info_type:
#         return session.query(PhoneInfoLog).filter(PhoneInfoLog.user_id == user_id,
#                                                   PhoneInfoLog.bank_branch_id == bank_branch_id)
#     if InfoTypes.address == info_type:
#         return session.query(AddressInfoLog).filter(AddressInfoLog.user_id == user_id,
#                                                     AddressInfoLog.bank_branch_id == bank_branch_id)
#     if InfoTypes.description == info_type:
#         return session.query(DescriptionInfoLog).filter(DescriptionInfoLog.user_id == user_id,
#                                                         DescriptionInfoLog.bank_branch_id == bank_branch_id)


def confirm_branch_info(user, info_type, liked_object):
    user = get_user(user.peer_id)
    if not liked_object:
        return 2
    liked_object_id = liked_object.id
    exist = session.query(Like).filter(Like.user_id == user.id, Like.liked_object_type == info_type,
                                       Like.liked_object_id == liked_object_id).one_or_none()
    if exist:
        return 1
    like = Like(user, info_type, liked_object_id, liked_object.bank_branch_id)
    liked_object.likes += 1
    session.add(like)
    session.commit()
    return 0


def generate_daily_report():
    # Create a workbook and add a worksheet.
    if not os.path.exists(BotConfig.reports_route):
        os.mkdir(BotConfig.reports_route)
    workbook = xlsxwriter.Workbook(BotConfig.reports_route + BotConfig.daily_report_filename)

    today_deleted_num = 0

    # LocationInfo
    worksheet = workbook.add_worksheet(name='location')
    today_deleted_locations = session.query(LocationInfoLog).filter(
        cast(LocationInfoLog.date_time, Date) == datetime.datetime.now().date()).all()
    today_deleted_num += today_deleted_locations.__len__()
    today_records = session.query(User, LocationInfo, BankBranch).filter(
        User.id == LocationInfo.user_id, LocationInfo.bank_branch_id == BankBranch.id,
        cast(LocationInfo.date_time, Date) == datetime.datetime.now().date()).all()
    today_locations_num = today_records.__len__()
    rs = []
    for record in today_records:
        rs.append(
            (record.BankBranch.branch_id, record.BankBranch.name, record.User.peer_id, record.User.user_name,
             record.LocationInfo.latitude,
             record.LocationInfo.longitude, record.LocationInfo.likes, record.LocationInfo.version,
             str(jdatetime.datetime.fromgregorian(datetime=record.LocationInfo.date_time))))
    header = (
        "branch_id", "branch_name", "user_id", "user_name", "latitude", "longitude", "confirm_count", "version",
        "datetime")
    row = 0
    worksheet.write_row(row, 0, header)
    row += 1
    for r in rs:
        worksheet.write_row(row, 0, r)
        row += 1
    worksheet.autofilter('A1:I1')

    # PhoneInfo
    worksheet = workbook.add_worksheet(name='phone')
    today_deleted_phones = session.query(PhoneInfoLog).filter(
        cast(PhoneInfoLog.date_time, Date) == datetime.datetime.now().date()).all()
    today_deleted_num += today_deleted_phones.__len__()
    today_records = session.query(User, PhoneInfo, BankBranch).filter(
        User.id == PhoneInfo.user_id, PhoneInfo.bank_branch_id == BankBranch.id,
        cast(PhoneInfo.date_time, Date) == datetime.datetime.now().date()).all()
    today_phones_num = today_records.__len__()
    rs = []
    for record in today_records:
        rs.append(
            (record.BankBranch.branch_id, record.BankBranch.name, record.User.peer_id, record.User.user_name,
             record.PhoneInfo.phone_number,
             record.PhoneInfo.likes, record.PhoneInfo.version,
             str(jdatetime.datetime.fromgregorian(datetime=record.PhoneInfo.date_time))))
    header = (
        "branch_id", "branch_name", "user_id", "user_name", "phone_number", "confirm_count", "version", "datetime")
    row = 0
    worksheet.write_row(row, 0, header)
    row += 1
    for r in rs:
        worksheet.write_row(row, 0, r)
        row += 1
    worksheet.autofilter('A1:H1')

    # AddressInfo
    worksheet = workbook.add_worksheet(name='address')
    today_deleted_address = session.query(AddressInfoLog).filter(
        cast(AddressInfoLog.date_time, Date) == datetime.datetime.now().date()).all()
    today_deleted_num += today_deleted_address.__len__()
    today_records = session.query(User, AddressInfo, BankBranch).filter(
        User.id == AddressInfo.user_id, AddressInfo.bank_branch_id == BankBranch.id,
        cast(AddressInfo.date_time, Date) == datetime.datetime.now().date()).all()
    today_address_num = today_records.__len__()
    rs = []
    for record in today_records:
        rs.append(
            (record.BankBranch.branch_id, record.BankBranch.name, record.User.peer_id, record.User.user_name,
             record.AddressInfo.address, record.AddressInfo.likes, record.AddressInfo.version,
             str(jdatetime.datetime.fromgregorian(datetime=record.AddressInfo.date_time))))
    header = ("branch_id", "branch_name", "user_id", "user_name", "address", "confirm_count", "version", "datetime")
    row = 0
    worksheet.write_row(row, 0, header)
    row += 1
    for r in rs:
        worksheet.write_row(row, 0, r)
        row += 1
    worksheet.autofilter('A1:H1')

    # DescriptionInfo
    worksheet = workbook.add_worksheet(name='description')
    today_deleted_description = session.query(DescriptionInfoLog).filter(
        cast(DescriptionInfoLog.date_time, Date) == datetime.datetime.now().date()).all()
    today_deleted_num += today_deleted_description.__len__()
    today_records = session.query(User, DescriptionInfo, BankBranch).filter(
        User.id == DescriptionInfo.user_id, DescriptionInfo.bank_branch_id == BankBranch.id,
        cast(DescriptionInfo.date_time, Date) == datetime.datetime.now().date()).all()
    today_description_num = today_records.__len__()
    rs = []
    for record in today_records:
        rs.append(
            (record.BankBranch.branch_id, record.BankBranch.name, record.User.peer_id, record.User.user_name,
             record.DescriptionInfo.description, record.DescriptionInfo.likes, record.DescriptionInfo.version,
             str(jdatetime.datetime.fromgregorian(datetime=record.DescriptionInfo.date_time))))
    header = ("branch_id", "branch_name", "user_id", "user_name", "description", "confirm_count", "version", "datetime")
    row = 0
    worksheet.write_row(row, 0, header)
    row += 1
    for r in rs:
        worksheet.write_row(row, 0, r)
        row += 1
    worksheet.autofilter('A1:H1')

    # Write a total using a formula.
    # worksheet.write(row, 0, 'Total')
    # worksheet.write(row, 1, '=SUM(B1:B4)')

    workbook.close()

    active_user_id_total = set()
    res = []
    res += session.query(Like.user_id).filter(cast(Like.date_time, Date) == datetime.datetime.now().date()).all()
    res += session.query(LocationInfo.user_id).filter(
        LocationInfo.user_id != 1, cast(LocationInfo.date_time, Date) == datetime.datetime.now().date()).all()
    res += session.query(PhoneInfo.user_id).filter(
        cast(PhoneInfo.date_time, Date) == datetime.datetime.now().date()).all()
    res += session.query(AddressInfo.user_id).filter(
        cast(AddressInfo.date_time, Date) == datetime.datetime.now().date()).all()
    res += session.query(DescriptionInfo.user_id).filter(
        cast(DescriptionInfo.date_time, Date) == datetime.datetime.now().date()).all()
    for r in res:
        active_user_id_total.add(r[0])

    active_bank_id_total = set()
    res = []
    res += session.query(Like.bank_branch_id).filter(cast(Like.date_time, Date) == datetime.datetime.now().date()).all()
    res += session.query(LocationInfo.bank_branch_id).filter(
        LocationInfo.user_id != 1, cast(LocationInfo.date_time, Date) == datetime.datetime.now().date()).all()
    res += session.query(PhoneInfo.bank_branch_id).filter(
        cast(PhoneInfo.date_time, Date) == datetime.datetime.now().date()).all()
    res += session.query(AddressInfo.bank_branch_id).filter(
        cast(AddressInfo.date_time, Date) == datetime.datetime.now().date()).all()
    res += session.query(DescriptionInfo.bank_branch_id).filter(
        cast(DescriptionInfo.date_time, Date) == datetime.datetime.now().date()).all()
    for r in res:
        active_bank_id_total.add(r[0])

    today_changes_num = today_locations_num + today_phones_num + today_address_num + today_description_num
    return active_user_id_total.__len__(), active_bank_id_total.__len__(), today_changes_num, today_deleted_num, \
           today_locations_num, today_phones_num, today_address_num, today_description_num


# generate_daily_report()


def generate_full_report():
    if not os.path.exists(BotConfig.reports_route):
        os.mkdir(BotConfig.reports_route)
    deleted_record_num = 0
    workbook = xlsxwriter.Workbook(BotConfig.reports_route + BotConfig.full_report_filename)

    worksheet = workbook.add_worksheet('location')
    # unique_records = session.query(LocationInfo).filter(LocationInfo.version == 1).all()
    # unique_records_num += unique_records.__len__()
    deleted_locations = session.query(LocationInfoLog).all()
    deleted_record_num += deleted_locations.__len__()
    records = session.query(User, LocationInfo, BankBranch).filter(
        User.id == LocationInfo.user_id, LocationInfo.bank_branch_id == BankBranch.id,
        LocationInfo.version > 0).all()
    total_changes_locations = records.__len__()
    rs = []
    for record in records:
        rs.append((record.BankBranch.branch_id, record.BankBranch.name, record.User.peer_id, record.User.user_name,
                   record.LocationInfo.latitude, record.LocationInfo.longitude, record.LocationInfo.likes,
                   record.LocationInfo.version,
                   str(jdatetime.datetime.fromgregorian(datetime=record.LocationInfo.date_time))))
    header = (
        "branch_id", "branch_name", "user_id", "user_name", "latitude", "longitude", "confirm_count", "version",
        "datetime")
    row = 0
    worksheet.write_row(row, 0, header)
    row += 1
    for r in rs:
        worksheet.write_row(row, 0, r)
        row += 1
    worksheet.autofilter('A1:I1')

    worksheet = workbook.add_worksheet('phone')
    # unique_records = session.query(PhoneInfo).filter(PhoneInfo.version == 1).all()
    # unique_records_num = unique_records.__len__()
    deleted_phones = session.query(PhoneInfoLog).all()
    deleted_record_num += deleted_phones.__len__()
    records = session.query(User, PhoneInfo, BankBranch).filter(
        User.id == PhoneInfo.user_id, PhoneInfo.bank_branch_id == BankBranch.id,
        PhoneInfo.version > 0).all()
    total_changes_phones = records.__len__()
    rs = []
    for record in records:
        rs.append((record.BankBranch.branch_id, record.BankBranch.name, record.User.peer_id, record.User.user_name,
                   record.PhoneInfo.phone_number, record.PhoneInfo.likes, record.PhoneInfo.version,
                   str(jdatetime.datetime.fromgregorian(datetime=record.PhoneInfo.date_time))))
    header = ("branch_id", "branch_name", "user_id", "user_name", "phone", "confirm_count", "version", "datetime")
    row = 0
    worksheet.write_row(row, 0, header)
    row += 1
    for r in rs:
        worksheet.write_row(row, 0, r)
        row += 1
    worksheet.autofilter('A1:H1')

    worksheet = workbook.add_worksheet('address')
    deleted_address = session.query(AddressInfoLog).all()
    deleted_record_num += deleted_address.__len__()
    records = session.query(User, AddressInfo, BankBranch).filter(
        User.id == AddressInfo.user_id, AddressInfo.bank_branch_id == BankBranch.id,
        AddressInfo.version > 0).all()
    total_changes_address = records.__len__()
    rs = []
    for record in records:
        rs.append((record.BankBranch.branch_id, record.BankBranch.name, record.User.peer_id, record.User.user_name,
                   record.AddressInfo.address, record.AddressInfo.likes, record.AddressInfo.version,
                   str(jdatetime.datetime.fromgregorian(datetime=record.AddressInfo.date_time))))
    header = ("branch_id", "branch_name", "user_id", "user_name", "address", "confirm_count", "version", "datetime")
    row = 0
    worksheet.write_row(row, 0, header)
    row += 1
    for r in rs:
        worksheet.write_row(row, 0, r)
        row += 1
    worksheet.autofilter('A1:H1')

    worksheet = workbook.add_worksheet('description')
    deleted_descriptions = session.query(DescriptionInfoLog).all()
    deleted_record_num += deleted_descriptions.__len__()
    records = session.query(User, DescriptionInfo, BankBranch).filter(
        User.id == DescriptionInfo.user_id, DescriptionInfo.bank_branch_id == BankBranch.id,
        DescriptionInfo.version > 0).all()
    total_changes_description = records.__len__()
    rs = []
    for record in records:
        rs.append((record.BankBranch.branch_id, record.BankBranch.name, record.User.peer_id, record.User.user_name,
                   record.DescriptionInfo.description, record.DescriptionInfo.likes, record.DescriptionInfo.version,
                   str(jdatetime.datetime.fromgregorian(datetime=record.DescriptionInfo.date_time))))
    header = ("branch_id", "branch_name", "user_id", "user_name", "description", "confirm_count", "version", "datetime")
    row = 0
    worksheet.write_row(row, 0, header)
    row += 1
    for r in rs:
        worksheet.write_row(row, 0, r)
        row += 1
    worksheet.autofilter('A1:H1')

    workbook.close()

    active_user_id_total = set()
    res = []
    res += session.query(Like.user_id).all()
    res += session.query(LocationInfo.user_id).filter(LocationInfo.user_id != 1).all()
    res += session.query(PhoneInfo.user_id).all()
    res += session.query(AddressInfo.user_id).all()
    res += session.query(DescriptionInfo.user_id).all()
    for r in res:
        active_user_id_total.add(r[0])

    active_bank_id_total = set()
    res = []
    res += session.query(Like.bank_branch_id).all()
    res += session.query(LocationInfo.bank_branch_id).filter(LocationInfo.user_id != 1).all()
    res += session.query(PhoneInfo.bank_branch_id).all()
    res += session.query(AddressInfo.bank_branch_id).all()
    res += session.query(DescriptionInfo.bank_branch_id).all()
    for r in res:
        active_bank_id_total.add(r[0])

    total_changes_num = total_changes_locations + total_changes_phones + \
                        total_changes_address + total_changes_description
    return active_user_id_total.__len__(), active_bank_id_total.__len__(), total_changes_num, deleted_record_num, \
           total_changes_locations, total_changes_phones, total_changes_address, total_changes_description
