from app.snuggproJob import SnuggProJob
import app.config

test_job = SnuggProJob('Steventest', 'Qiantest', 'stevenqiantest@gmail.com', '(434) 995-5587', '755 Prospect Ave', 'Charlottesville', 'VA', '22903')

test_job.create_job()
