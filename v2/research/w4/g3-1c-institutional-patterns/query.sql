SELECT DISTINCT p.role FROM episode e JOIN profile p ON p.id=e.profile
 WHERE e.holder=:holder AND e.scope=p.scope AND e.jurisdiction=:jurisdiction
 AND e.start_day<=:day AND (e.end_day IS NULL OR :day<e.end_day) ORDER BY p.role;