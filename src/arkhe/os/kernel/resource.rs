// src/arkhe/os/kernel/resource.rs

pub struct FdPerms {
    read: bool,
    write: bool,
}

pub struct TemporalAnchor {
    timestamp: u64,
}

pub struct TemporalChain;
impl TemporalChain {
    pub fn anchor(action: &str, id: u64) -> TemporalAnchor {
        TemporalAnchor { timestamp: 0 }
    }
}

/// Recurso linear: não pode ser clonado, deve ser consumido exatamente uma vez.
pub struct Fd<T> {
    id: u64,
    resource: T,
    permissions: FdPerms,
    anchor: Option<TemporalAnchor>,
}

impl<T> Fd<T> {
    /// Consome o recurso e retorna seu conteúdo, ancorando a operação.
    pub fn consume(self) -> (T, TemporalAnchor) {
        let anchor = TemporalChain::anchor("fd_consumed", self.id);
        (self.resource, anchor)
    }
}
