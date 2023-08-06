import click
import time

from contextlib import contextmanager

def info(message, **vargs):
  click.echo(message, **vargs)

def unimportant(message, **vargs):
  click.secho(message, fg='cyan', **vargs)

def error(message, **vargs):
  click.secho(message, fg='red')

def panic(message, status=1, **vargs):
  error(message, **vargs)
  exit(status)

@contextmanager
def fake_progress(eta, half_life, *args, **vargs):
  """
  Retuns an approximate progress bar

  Progress is 90% after 'eta' seconds.  The remaining progress halves
  every 'half_life' seconds.
  """
  vargs['length'] = 100
  with click.progressbar(*args, **vargs) as bar:
    previous_progress = 0
    started = time.time()
    def tick():
      nonlocal previous_progress
      elapsed = time.time() - started
      if elapsed < eta:
        progress = 90 * elapsed / eta
      else:
        overdue = elapsed - eta
        progress = 100 - 10 * (0.5 ** (overdue / half_life))
      
      bar.update(progress - previous_progress)
      previous_progress = progress
    
    yield tick