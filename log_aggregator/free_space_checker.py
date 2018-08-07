import psutil


def check_disk_available(gb_availabe_min=1):
    available_space = psutil.disk_usage('/')[2]
    available_space_gb = available_space * 10e-10
    return available_space_gb, available_space_gb > gb_availabe_min