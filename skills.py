from datetime import datetime
from storage import StorageHandler

VALID_STAGES = ["TO_LEARN", "LEARNING", "PRACTICING", "DONE", "REVISE"]

class SkillManager:
    def __init__(self, filepath=r"D:\tracker-skills\skills.json"):
        self.storage = StorageHandler(filepath)
        self.skills = self.storage.load_data()

    def _save(self):
        self.storage.save_data(self.skills)

    def _get_timestamp(self):
        return datetime.now().isoformat(timespec='seconds')

    def add_skill(self, name, tags=None):
        if name in self.skills:
            raise ValueError(f"Skill '{name}' already exists.")
        
        self.skills[name] = {
            "name": name,
            "stage": "TO_LEARN",
            "notes": "",
            "sub_skills": [],
            "tags": tags or [],
            "last_updated": self._get_timestamp()
        }
        self._save()
        return self.skills[name]

    def move_skill(self, name, stage):
        if name not in self.skills:
            raise ValueError(f"Skill '{name}' not found.")
        stage = stage.upper()
        if stage not in VALID_STAGES:
            raise ValueError(f"Invalid stage '{stage}'. Must be one of: {', '.join(VALID_STAGES)}")
        
        self.skills[name]["stage"] = stage
        self.skills[name]["last_updated"] = self._get_timestamp()
        self._save()
        return self.skills[name]

    def push_skill(self, name):
        if name not in self.skills:
            raise ValueError(f"Skill '{name}' not found.")
        
        current_stage = self.skills[name]["stage"]
        current_index = VALID_STAGES.index(current_stage)
        
        if current_index >= len(VALID_STAGES) - 1:
            raise ValueError(f"Skill '{name}' is already at the final stage '{current_stage}'.")
            
        next_stage = VALID_STAGES[current_index + 1]
        self.skills[name]["stage"] = next_stage
        self.skills[name]["last_updated"] = self._get_timestamp()
        self._save()
        return self.skills[name]

    def add_note(self, name, text):
        if name not in self.skills:
            raise ValueError(f"Skill '{name}' not found.")
        
        self.skills[name]["notes"] = text
        self.skills[name]["last_updated"] = self._get_timestamp()
        self._save()
        return self.skills[name]

    def add_sub_skill(self, name, text):
        if name not in self.skills:
            raise ValueError(f"Skill '{name}' not found.")
        
        sub_skill = {
            "text": text
        }
        if "sub_skills" not in self.skills[name]:
            self.skills[name]["sub_skills"] = []
            
        self.skills[name]["sub_skills"].append(sub_skill)
        self._save()
        return self.skills[name]

    def view_skill(self, name):
        if name not in self.skills:
            raise ValueError(f"Skill '{name}' not found.")
        return self.skills[name]

    def delete_skill(self, name):
        if name not in self.skills:
            raise ValueError(f"Skill '{name}' not found.")
        del self.skills[name]
        self._save()

    def list_skills(self, stage=None):
        if stage:
            stage = stage.upper()
            return {k: v for k, v in self.skills.items() if v["stage"] == stage}
        return self.skills
