from src.core.entities import SkillsSet


def test_skills_match_and_missing():
    have = SkillsSet(["Python", "Django", "GraphQL"]) 
    need = SkillsSet(["python", "React", "GraphQL"]) 
    assert have.matched_with(need) == ["graphql", "python"]
    assert have.missing_from(need) == ["react"]