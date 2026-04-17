-- Simplified investor form now only collects full_name + email.
-- Make all other columns nullable so the simplified submission doesn't fail.

DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'investor_interest' AND column_name = 'linkedin') THEN
    EXECUTE 'ALTER TABLE investor_interest ALTER COLUMN linkedin DROP NOT NULL';
  END IF;
  IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'investor_interest' AND column_name = 'investing_experience') THEN
    EXECUTE 'ALTER TABLE investor_interest ALTER COLUMN investing_experience DROP NOT NULL';
  END IF;
  IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'investor_interest' AND column_name = 'domain_expertise') THEN
    EXECUTE 'ALTER TABLE investor_interest ALTER COLUMN domain_expertise DROP NOT NULL';
  END IF;
  IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'investor_interest' AND column_name = 'value_add') THEN
    EXECUTE 'ALTER TABLE investor_interest ALTER COLUMN value_add DROP NOT NULL';
  END IF;
  IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'investor_interest' AND column_name = 'commitment_amount') THEN
    EXECUTE 'ALTER TABLE investor_interest ALTER COLUMN commitment_amount DROP NOT NULL';
  END IF;
  IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'investor_interest' AND column_name = 'notes') THEN
    EXECUTE 'ALTER TABLE investor_interest ALTER COLUMN notes DROP NOT NULL';
  END IF;
END $$;
