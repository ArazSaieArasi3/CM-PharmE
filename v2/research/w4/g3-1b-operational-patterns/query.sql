SELECT DISTINCT c.facet FROM context c JOIN role_profile r ON r.role=c.role
WHERE c.role=:role AND c.holder=:holder AND c.scope=r.scope
 AND c.jurisdiction=:jurisdiction AND c.start_day<=:day
 AND (c.end_day IS NULL OR :day<c.end_day)
 AND c.facet IN ('authorization','responsibility','activity') ORDER BY c.facet;