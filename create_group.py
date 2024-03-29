# Tên các nhóm
group_names = ['group1', 'group2', 'group3', 'group4', 'group5']  # Thêm tên nhóm cần tạo vào đây

# Tạo các nhóm cho Redis Stream
for group_name in group_names:
    try:
        # Kiểm tra xem nhóm đã tồn tại chưa
        group_info = redis_conn.xinfo_groups(stream_name)
        existing_groups = [group['name'] for group in group_info]
        if group_name not in existing_groups:
            redis_conn.xgroup_create(stream_name, group_name, id='0', mkstream=True)
    except Exception as e:
        app.logger.error("Error while creating group '%s': %s", group_name, str(e))
