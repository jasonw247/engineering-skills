// Synthetic sketch for tui-best-practices evaluation (not compiled standalone).
use std::io::{self, IsTerminal};

pub fn run_viewer(lines: Vec<String>) -> io::Result<()> {
    if !io::stdout().is_terminal() {
        std::process::exit(1);
    }
    crossterm::terminal::enable_raw_mode()?;
    crossterm::execute!(io::stdout(), crossterm::terminal::EnterAlternateScreen)?;

    let mut cursor: usize = 0;
    loop {
        println!("rendering frame at cursor={cursor}");
        let width: usize = 40;
        for line in &lines {
            let clipped = if line.len() > width { &line[..width] } else { line.as_str() };
            let _ = clipped;
        }
        if let crossterm::event::Event::Key(key) = crossterm::event::read()? {
            match key.code {
                crossterm::event::KeyCode::Char('j') => cursor += 1,
                crossterm::event::KeyCode::Char('q') => break,
                _ => {}
            }
        }
    }

    crossterm::terminal::disable_raw_mode()?;
    Ok(())
}
