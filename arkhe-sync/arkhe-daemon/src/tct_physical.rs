// No arquivo src/tct_physical.rs (adicionado ao covm-daemon)
use std::fs::File;
use std::os::fd::AsRawFd;
use nix::{ioctl_write_ptr_bad, ioctl_read_bad};

ioctl_write_ptr_bad!(tct_set_freq, 0x01, u64);
ioctl_write_ptr_bad!(tct_set_phase, 0x02, u64);
ioctl_write_ptr_bad!(tct_set_tau, 0x03, u64);
ioctl_write_ptr_bad!(tct_trigger, 0x04, u32);
ioctl_read_bad!(tct_get_lambda2, 0x10, u64);

pub struct TCTPhysical {
    dev: File,
}

impl TCTPhysical {
    pub fn open(path: &str) -> Result<Self, std::io::Error> {
        let dev = File::open(path)?;
        Ok(TCTPhysical { dev })
    }

    pub fn set_frequency(&self, freq_hz: u64) {
        unsafe { tct_set_freq(self.dev.as_raw_fd(), &freq_hz).unwrap(); }
    }

    pub fn set_phase(&self, phase: f64) {
        let p = (phase * 1e6) as u64;
        unsafe { tct_set_phase(self.dev.as_raw_fd(), &p).unwrap(); }
    }

    pub fn set_tau(&self, tau: f64) {
        let t = tau.to_bits();
        unsafe { tct_set_tau(self.dev.as_raw_fd(), &t).unwrap(); }
    }

    pub fn trigger(&self) {
        unsafe { tct_trigger(self.dev.as_raw_fd(), &0).unwrap(); }
    }

    pub fn measure(&self) -> f64 {
        let mut lambda2: u64 = 0;
        unsafe { tct_get_lambda2(self.dev.as_raw_fd(), &mut lambda2).unwrap(); }
        f64::from_bits(lambda2)
    }
}
