import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const body = await req.json();

    const supabase = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
    );

    const insertData: Record<string, unknown> = {
      full_name: body.full_name,
      email: body.email,
    };
    if (body.linkedin) insertData.linkedin = body.linkedin;
    if (body.investing_experience) insertData.investing_experience = body.investing_experience;
    if (body.domain_expertise) insertData.domain_expertise = body.domain_expertise;
    if (body.value_add) insertData.value_add = body.value_add;
    if (body.commitment_amount) insertData.commitment_amount = body.commitment_amount;
    if (body.notes) insertData.notes = body.notes;

    const { error } = await supabase.from("investor_interest").insert(insertData);

    if (error) throw error;

    return new Response(JSON.stringify({ success: true }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 400,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
