use std::collections::HashMap;

#[derive(Clone)]
pub struct DistilledSkill {
    pub pattern_hash: [u8; 32],
    pub efficiency_gain: f64,
    pub usage_count: u32,
}

pub struct SkillDistillery {
    patterns: HashMap<[u8; 32], DistilledSkill>,
    occurrence_threshold: u32,
}

impl SkillDistillery {
    pub fn new() -> Self {
        Self {
            patterns: HashMap::new(),
            occurrence_threshold: 100,
        }
    }

    pub fn observe(&mut self, hash: [u8; 32]) -> Option<DistilledSkill> {
        if let Some(skill) = self.patterns.get_mut(&hash) {
            skill.usage_count += 1;
            return Some(skill.clone());
        } else {
            self.patterns.insert(hash, DistilledSkill {
                pattern_hash: hash,
                efficiency_gain: 0.0,
                usage_count: 1,
            });
            None
        }
    }

    pub fn distill(&mut self, hash: &[u8; 32]) -> Option<DistilledSkill> {
        let skill = self.patterns.get(hash)?;
        if skill.usage_count >= self.occurrence_threshold && skill.efficiency_gain == 0.0 {
            let mut distilled = skill.clone();
            distilled.efficiency_gain = 0.35;
            self.patterns.insert(*hash, distilled.clone());
            return Some(distilled);
        }
        None
    }
}
