INSERT INTO accounts (email, password_hash, role)
VALUES ('turing@docman.com', '$2b$12$k3fsOiDkDQBlzB.80YOkc.YYwFsqDZXveZu.yQ7h5LFkpG7cJ3qvC', 'viewer'),
	   ('lovelace@docman.com', '$2b$12$9yqwEZA/sGVVrXplX5cL0.7Nt49HsQxBZPHXWsRS4daBqRWOwjPSO', 'reviewer'),
	   ('linus@docman.com', '$2b$12$8yKPRAqg5UQhKjPYUtcT8enA7tjU9anXyuqoKbL0JFl2VXtaG57qy', 'manager'),
	   ('stallman@docman.com', '$2b$12$ADE6eNkEt00fbRpE1px1p.zFEOLScvTPzOxptFy.ZdmN0YJmT9yZu', 'admin');