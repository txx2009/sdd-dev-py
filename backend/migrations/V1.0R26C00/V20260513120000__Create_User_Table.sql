-- V20260513120000__Create_User_Table.sql
CREATE TABLE IF NOT EXISTS t_user (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    nickname VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    status TINYINT NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- 初始管理员账户 (密码: admin123, BCrypt加密)
INSERT INTO t_user (username, password, nickname, email, phone, status, created_at)
SELECT 'admin', '$2a$10$BScxd/KzBW.lU.a/XP6HGe4ArF.Y9xUj7wsgma2IjHBPdbBhnaZDm', '管理员', 'admin@example.com', '13800138000', 1, CURRENT_TIMESTAMP
WHERE NOT EXISTS (SELECT 1 FROM t_user WHERE username = 'admin');
