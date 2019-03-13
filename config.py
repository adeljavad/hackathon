import os


class BotConfig:
    daily_last_version_report_filename = "daily_last_versions_report.xlsx"
    daily_report_filename = "daily_report.xlsx"
    full_report_filename = "full_report.xlsx"
    reports_route = "files/"
    admins = ['1630184172']
    base_url = os.environ.get('BASE_URL', None) or "https://tapi.bale.ai/"
    bot_token = os.environ.get('TOKEN', None) or "1239525175:e523a3ce66aae472c159d110ca4a24541f129a51"
    system_local = os.environ.get('SYSTEM_LOCAL', None) or "fa_IR"
    resending_max_try = int(os.environ.get('RESENDING_MAX_TRY', 5))
    reuploading_max_try = int(os.environ.get('REUPLOADING_MAX_TRY', 5))
    location_guid_photo = {
      "$type": "Document",
      "fileId": "-1431652100289329405",
      "accessHash": "1471278867",
      "fileSize": "572065",
      "name": "location_guid.jpg",
      "mimeType": "image/jpeg",
      "thumb": {
        "width": 90,
        "height": 78,
        "thumb": "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"
      },
      "ext": {
        "$type": "Photo",
        "width": 1510,
        "height": 1318
      }}


class DbConfig:
    # db_user = os.environ.get('POSTGRES_USER', "adel")
    # db_password = os.environ.get('POSTGRES_PASSWORD', "9347")
    # db_host = os.environ.get('POSTGRES_HOST', "(local)")
    # db_name = os.environ.get('POSTGRES_DB', "loc")
    # db_port = os.environ.get('POSTGRES_PORT', "1433")
    # database_url = "mssql+pyodbc://{}:{}@{}:{}/{}".format(db_user, db_password, db_host, db_port, db_name) or None
    #
    pass