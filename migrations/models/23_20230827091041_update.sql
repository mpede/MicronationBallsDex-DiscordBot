-- upgrade --
ALTER TABLE "ball" DROP COLUMN "location";
-- downgrade --
ALTER TABLE "ball" ADD "location" VARCHAR(60) NOT NULL;
